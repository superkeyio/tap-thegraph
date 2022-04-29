"""Stream type classes for tap-thegraph."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable
import stringcase

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_thegraph.client import TheGraphStream
from graphql import GraphQLInterfaceType, get_introspection_query, GraphQLObjectType

# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")
# TODO: - Override `UsersStream` and `GroupsStream` with your own stream definition.
#       - Copy-paste as many times as needed to create multiple stream types.

# TODO: heavy lifting here
def convert_graphql_output_type_to_schema(graphql_output_type):
    pass

class EntityStream(TheGraphStream):
    entity: Union[GraphQLObjectType, GraphQLInterfaceType]

    @property
    def name(self) -> str:
        return self.entity.name

    def __init__(self, *args, **kwargs):
        self.entity = kwargs.pop('entity')
        super().__init__(*args, **kwargs)

    @property
    def schema(self) -> dict:
        properties: List[th.Property] = []

        return th.PropertiesList(*properties).to_dict()

    @property
    def query(self) -> str:
        return ""
    

    