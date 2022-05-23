"""Stream type classes for tap-thegraph."""

import json
from operator import index
from pprint import pprint
from typing import Any, Dict, Iterable, Optional
from pyparsing import indentedBlock

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_thegraph.client import SubgraphStream
from copy import deepcopy
import requests
from stringcase import camelcase

# How to debug easier?
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
        "type": "integer"
    },
    "Address": {
        "type": "string",
        "minLength": 40,
        "maxLength": 40
    },
}

foreign_key_type = {
    "type": "object",
    "properties": {
        "id": {
            "type": "string",
        }
    }
}


class EntityStream(SubgraphStream):
    primary_keys = ["id"]

    entity_name: str

    _latest_order_attribute_value: Any = None
    _next_page_token: Any = None

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

        def normalize_schema(node: dict):
            iterator = None
            if isinstance(node, list):
                iterator = range(len(node))
            elif isinstance(node, dict):
                iterator = node.keys()
            if iterator:
                for child in iterator:
                    normalize_schema(node[child])
                    if isinstance(node[child], dict):
                        if '$ref' in node[child]:
                            ref_type = node[child]['$ref'].split('/')[-1]
                            node[child] = graph_type_to_json_schema_type.get(
                                ref_type, foreign_key_type)
                        elif "properties" in node[child] and "return" in node[
                                child]["properties"]:
                            node[child] = node[child]["properties"]["return"]

        normalize_schema(entity_definition)
        return entity_definition

    @property
    def schema(self) -> dict:
        return self._extract_entity_schema_from_api_schema(self.entity_name)

    @property
    def query_type(self) -> str:
        # TODO: how to pluralize this?
        return f"{camelcase(self.entity_name)}s"

    @property
    def order_attribute(self) -> str:
        return self.replication_key if self.replication_key else 'id'

    @property
    def order_attribute_type(self) -> str:
        return self.schema["properties"][self.order_attribute]["title"]

    # https://thegraph.com/docs/en/developer/graphql-api/#pagination
    def get_url_params(self, context: Optional[dict],
                       next_page_token: Optional[Any]) -> Dict[str, Any]:
        return {
            "batchSize": 1000,
            "latestOrderValue": self._latest_order_attribute_value
        }

    def get_next_page_token(self, response: requests.Response,
                            previous_token: Optional[Any]) -> Any:
        return self._next_page_token

    @property
    def query(self) -> str:
        newline = "\n\t"
        return f"""
query($batchSize: Int!{ f', $latestOrderValue: {self.order_attribute_type}!' if self._latest_order_attribute_value else '' }) {{
    {self.query_type}(first: $batchSize, orderBy: {self.order_attribute}, orderDirection: asc{f', where: {{ {self.order_attribute}_gt: $latestOrderValue }}' if self._latest_order_attribute_value else ''}) {{
        {newline.join(self.schema["properties"].keys())}
    }}
}}
"""

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        rows = response.json()["data"][self.query_type]
        for row in rows:
            yield row
            self._latest_order_attribute_value = row.get(self.order_attribute)

        self._next_page_token = None if len(
            rows) == 0 else self._latest_order_attribute_value
