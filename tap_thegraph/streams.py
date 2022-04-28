"""Stream type classes for tap-thegraph."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_thegraph.client import TheGraphStream
from graphql import get_introspection_query, GraphQLObjectType

# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")
# TODO: - Override `UsersStream` and `GroupsStream` with your own stream definition.
#       - Copy-paste as many times as needed to create multiple stream types.

class EntityStream(TheGraphStream):
    entity: GraphQLObjectType = None

    @property
    def name(self) -> str:
        return self.entity.name

    def __init__(self, *args, **kwargs):
        self.entity = kwargs.pop('entity')
        super().init(*args, **kwargs)

    