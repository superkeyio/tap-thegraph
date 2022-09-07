"""Stream type classes for tap-thegraph."""

from typing import Any, Dict, Iterable, Optional, Set

from functools import cached_property

from tap_thegraph.client import SubgraphStream
from copy import deepcopy
import requests
from stringcase import camelcase
import inflect

p = inflect.engine()

# TODO: incremental still doesn't work


# https://stackoverflow.com/questions/43587505/how-to-find-how-many-level-of-dictionary-is-there-in-python
def max_depth(d):
    if not isinstance(d, dict) or not d:
        return 0
    else:
        return max(max_depth(v) for k, v in d.items()) + 1


# https://thegraph.com/docs/en/developer/assemblyscript-api/#built-in-types
the_graph_builtin_type_to_json_schema_type = {
    "Boolean": {"type": ["boolean"]},
    "BigDecimal": {"type": ["string"]},
    "BigInt": {"type": ["string"]},
    "Bytes": {"type": ["string"]},
    "ID": {"type": ["string"]},
    "String": {"type": ["string"]},
    "ByteArray": {"type": ["string"]},
    "TypedMap": {"type": ["object"]},
    "Int": {"type": ["integer"]},
    "Address": {"type": ["string"], "minLength": 40, "maxLength": 40},
}

foreign_key_type = {"type": ["string"]}
enum_key_type = {"type": ["string"]}


def common_iterable(obj):
    if isinstance(obj, dict):
        for key in obj:
            yield key
    elif isinstance(obj, list):
        for index, _ in enumerate(obj):
            yield index
    return None


class EntityStream(SubgraphStream):
    primary_keys = ["id"]

    entity_name: str

    batch_size: int

    _latest_order_attribute_value: Any
    _next_page_token: Any

    STATE_MSG_FREQUENCY = 100

    entity_config: dict

    @cached_property
    def name(self) -> str:
        return f"{self.subgraph_name}.{self.entity_name}"

    @property
    def entity_name(self) -> str:
        return self.entity_config.get("name")

    def __init__(self, *args, **kwargs):
        self.entity_config = kwargs.pop("entity_config")

        self._latest_order_attribute_value = self.entity_config.get("since")

        super().__init__(*args, **kwargs)

        self.replication_key = self.entity_config.get("created_at")

    def _extract_entity_schema_from_api_schema(self, entity_name: str) -> dict:
        entity_definition = deepcopy(self.api_json_schema["definitions"][entity_name])

        enums = self._get_enums(self.api_json_schema["definitions"])
        self._normalize_schema(entity_definition, enums)

        for property in entity_definition["properties"]:
            if property not in entity_definition["required"]:
                entity_definition["properties"][property]["type"].append("null")

        return entity_definition

    def _get_enums(self, definitions: Any) -> Set:
        return {k for k, v in definitions.items() if "anyOf" in v}

    def _normalize_schema(self, node: Any, enums: Set):
        iterator = common_iterable(node)
        if iterator:
            for child in iterator:
                self._normalize_schema(node[child], enums)
                if isinstance(node[child], dict):
                    if "$ref" in node[child]:
                        ref_type = node[child]["$ref"].split("/")[-1]
                        if ref_type in the_graph_builtin_type_to_json_schema_type:
                            node[child] = {
                                **deepcopy(
                                    the_graph_builtin_type_to_json_schema_type[ref_type]
                                ),
                                "description": ref_type,
                            }
                        elif ref_type in enums:
                            node[child] = {
                                **deepcopy(enum_key_type),
                                "description": ref_type,
                            }
                        else:
                            node[child] = {
                                **deepcopy(foreign_key_type),
                                "description": f"{ref_type}.id",
                            }
                    elif (
                        "properties" in node[child]
                        and "return" in node[child]["properties"]
                    ):
                        node[child] = node[child]["properties"]["return"]

    @cached_property
    def schema(self) -> dict:
        return self._extract_entity_schema_from_api_schema(self.entity_name)

    @cached_property
    def query_type(self) -> str:
        return p.plural_noun(camelcase(self.entity_name))

    @cached_property
    def order_attribute(self) -> str:
        return self.replication_key if self.replication_key else "id"

    @cached_property
    def order_attribute_type(self) -> str:
        return self.schema["properties"][self.order_attribute]["description"]

    # https://thegraph.com/docs/en/developer/graphql-api/#pagination
    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        return {
            "batchSize": self.config.get("batch_size"),
            "lastOrderAttributeValue": max(
                self._latest_order_attribute_value or "0",
                self.get_starting_replication_key_value(context) or "0",
            ),
        }

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Any:
        return self._next_page_token

    @property
    def query_fields(self) -> str:
        return (
            f"{k} {{ id }}"
            if max_depth(v) > 1 or ".id" in v.get("description", "")
            else k
            for k, v in self.schema["properties"].items()
        )

    @property
    def query(self) -> str:
        newline = "\n\t"
        query = f"""
query($batchSize: Int!{ f', $lastOrderAttributeValue: {self.order_attribute_type}!' if self._latest_order_attribute_value else '' }) {{
    {self.query_type}(first: $batchSize, orderBy: {self.order_attribute}, orderDirection: asc{f', where: {{ {self.order_attribute}_gt: $lastOrderAttributeValue }}' if self._latest_order_attribute_value else ''}) {{
        {newline.join(self.query_fields)}
    }}
}}
"""
        self.logger.info(query)
        return query

    def validate_response(self, response: requests.Response) -> None:
        if response.status_code == 400:
            print(response.json())
        return super().validate_response(response)

    def _flatten_foreign_key(self, node):
        if isinstance(node, dict) and list(node.keys()) == ["id"]:
            return node["id"]

        iterator = common_iterable(node)
        if iterator:
            for child in iterator:
                node[child] = self._flatten_foreign_key(node[child])

        return node

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        response_json = response.json()
        data = response_json.get("data")
        if data:
            rows = data.get(self.query_type)
            for row in rows:
                row = {k: self._flatten_foreign_key(v) for k, v in row.items()}
                yield row
                self._latest_order_attribute_value = row.get(self.order_attribute)

            self._next_page_token = (
                None if len(rows) == 0 else self._latest_order_attribute_value
            )
        else:
            self._next_page_token = None
