"""Stream type classes for tap-thegraph."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_thegraph.client import SubgraphStream
import json
from copy import deepcopy

# https://thegraph.com/docs/en/developer/assemblyscript-api/#built-in-types
graph_type_to_json_schema_type = {
    "BigDecimal": {
        "type": "number"
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

    @property
    def name(self) -> str:
        return f"{self.subgraph_name}_{self.entity_name}"

    replication_key: Optional[str] = None

    def __init__(self, *args, **kwargs):
        self.entity_name = kwargs.pop('entity_name')
        self.replication_key = kwargs.pop('replication_key')  # timestamp
        super().__init__(*args, **kwargs)

    @property
    def schema(self) -> dict:
        # TODO: clean up code
        entity_definition = deepcopy(
            self.api_json_schema["definitions"][self.entity_name])
        properties = entity_definition["properties"]
        for property in properties:
            properties[property] = properties[property]["properties"]["return"]
            properties[property].update(
                graph_type_to_json_schema_type[properties[property]['title']])
        return entity_definition

    @property
    def query(self) -> str:
        return ""
