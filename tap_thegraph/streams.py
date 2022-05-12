"""Stream type classes for tap-thegraph."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable
import stringcase

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_thegraph.client import TheGraphStream
from graphql import GraphQLEnumType, GraphQLInterfaceType, GraphQLNonNull, GraphQLOutputType, GraphQLScalarType, GraphQLUnionType, GraphQLWrappingType, get_introspection_query, GraphQLObjectType

# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")
# TODO: - Override `UsersStream` and `GroupsStream` with your own stream definition.
#       - Copy-paste as many times as needed to create multiple stream types.

# TODO: heavy lifting here
def convert_graphql_output_type_to_schema(graphql_output_type: GraphQLOutputType):
    
    if isinstance(graphql_output_type, GraphQLScalarType):
        print('Scalar', graphql_output_type)
        return dict(wrapped=th.StringType)
    elif isinstance(graphql_output_type, GraphQLObjectType) or isinstance(graphql_output_type, GraphQLInterfaceType):
        print('Object', graphql_output_type)
        properties: List[th.Property] = []
        for name, field in graphql_output_type.fields.items():
            properties.append(th.Property(name, **convert_graphql_output_type_to_schema(field.type)))
        return th.ObjectType(*properties)
    elif isinstance(graphql_output_type, GraphQLEnumType):
        print('Enum', graphql_output_type)
        pass
    elif isinstance(graphql_output_type, GraphQLUnionType):
        print('Union', graphql_output_type)
        pass
    elif isinstance(graphql_output_type, GraphQLNonNull):
        print('Wrapping', graphql_output_type)
        return dict(wrapped=th.StringType, required=True)

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
        r: th.ObjectType = convert_graphql_output_type_to_schema(self.entity)
        print(r.type_dict)
        return r.to_dict()

    @property
    def query(self) -> str:
        return ""
    

    