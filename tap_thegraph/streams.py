"""Stream type classes for tap-thegraph."""

from typing import Iterable, Optional

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_thegraph.client import SubgraphStream
from copy import deepcopy
import requests
from stringcase import camelcase

# https://thegraph.com/docs/en/developer/assemblyscript-api/#built-in-types
graph_type_to_json_schema_type = {
    "BigDecimal": {
        "type": "string"
    },
    "BigInt": {
        "type": "integer"
    },
    "Bytes": {
        "type": "string",
    },
    "ID": {
        "type": "string"
    },
    "String": {
        "type": "string"
    },
    "ByteArray": {
        "type": "string",
    },
    "TypedMap": {
        "type": "object"
    },
    "Int": {
        "type": "number"
    },
    "Address": {
        "type": "string",
        "minLength": 40,
        "maxLength": 40
    }
}


class EntityStream(SubgraphStream):
    entity_name: str
    entity_schema: dict

    primary_keys = ["id"]

    _latest_id: str = None
    _latest_timestamp: int = None

    @property
    def name(self) -> str:
        return f"{self.subgraph_name}_{self.entity_name}"

    replication_key: Optional[str] = None

    def __init__(self, *args, **kwargs):
        self.entity_name = kwargs.pop('entity_name')
        self.replication_key = kwargs.pop('replication_key')  # timestamp

        super().__init__(*args, **kwargs)

    def _extract_entity_schema_from_api_schema(self, entity_name: str) -> dict:
        entity_definition = deepcopy(
            self.api_json_schema["definitions"][entity_name])
        properties = entity_definition["properties"]
        for property in properties:
            properties[property] = properties[property]["properties"]["return"]
            properties[property].update(
                graph_type_to_json_schema_type[properties[property]['title']])
        return entity_definition

    @property
    def schema(self) -> dict:
        return self._extract_entity_schema_from_api_schema(self.entity_name)

    @property
    def query_type(self) -> str:
        # TODO: how to pluralize this?
        return f"{camelcase(self.entity_name)}s"

    @property
    def order_by(self) -> str:
        return self.replication_key if self.replication_key else 'id'

    # def get_url_params(self, context: Optional[dict], next_page_token: Optional[Any]) -> Dict[str, Any]:
    #     return super().get_url_params(context, next_page_token)

    # def get_next_page_token(self, response: requests.Response, previous_token: Optional[Any]) -> Any:
    #     return super().get_next_page_token(response, previous_token)

    @property
    def query(self) -> str:
        # TODO: how to do pagination?
        newline = "\n\t"
        q = f"""
query {{
    {self.query_type}(first: 1000, orderBy: {self.order_by}, orderDirection: asc) {{
        {newline.join(self.schema["properties"].keys())}
    }}
}}
"""
        print(q)
        return q

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        resp_json = response.json()
        for row in resp_json.get("data").get(self.query_type):
            yield row
