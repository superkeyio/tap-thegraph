"""Stream type classes for tap-thegraph."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable
import stringcase
import subprocess
import jsonref
from pprint import pprint

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_thegraph.client import TheGraphStream
from graphql import GraphQLEnumType, GraphQLInterfaceType, GraphQLNonNull, GraphQLOutputType, GraphQLScalarType, GraphQLUnionType, GraphQLWrappingType, get_introspection_query, GraphQLObjectType
import json

graphql_title_to_json_schema_type = {
    "BigDecimal": {},
    "Bytes": {},
    "BigInt": {},
    "Bytes": {},
    "ID": {},
    "String": {}
}

class EntityStream(TheGraphStream):
    entity: Union[GraphQLObjectType, GraphQLInterfaceType]
        
    @property
    def name(self) -> str:
        return self.entity.name

    replication_key: Optional[str] = None

    def __init__(self, *args, **kwargs):
        self.entity = kwargs.pop('entity')
        self.replication_key = kwargs.pop('replication_key') # timestamp
        super().__init__(*args, **kwargs)

    @property
    def schema(self) -> dict:
        # TODO: convert GraphQL schema to JSON schema and filter

        json_schema = jsonref.loads(subprocess.run(['subgraph-to-json-schema', self.graphql_client.transport.url], stdout=subprocess.PIPE).stdout.decode('utf-8'))
        entity_definition = json_schema["definitions"][self.entity.name]
        for property in entity_definition["properties"]:
            entity_definition["properties"][property] = entity_definition["properties"][property]["properties"]["return"]
        pprint(entity_definition)
        return { '': "" }


    @property
    def query(self) -> str:
        return ""
    

    