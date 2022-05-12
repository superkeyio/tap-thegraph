"""TheGraph tap class."""

import logging
from typing import Dict, List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers
# TODO: Import your custom stream types here:
from tap_thegraph.streams import (
    TheGraphStream,
    EntityStream,
)
from graphql import GraphQLInterfaceType, GraphQLObjectType, get_introspection_query, graphql_sync
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport, log as requests_logger

class TapTheGraph(Tap):
    """TheGraph tap class."""
    name = "tap-thegraph"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "subgraph_url",
            th.StringType,
            required=True,
        ),
        th.Property(
            "enitities",
            th.ArrayType(
                th.ObjectType(
                    th.Property("name", th.StringType, required=True),
                    th.Property("replication_key", th.StringType, description="Name of the field used for incremental replication (i.e. timestamp)")
                )
            )
        )

    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        requests_logger.setLevel(logging.WARNING)
        transport = RequestsHTTPTransport(
            url=self.config.get("subgraph_url"),
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)
        noop_query = """
        {
            __schema {
                queryType {
                    name
                }
            }
        }
        """
        client.execute(gql(noop_query))

        entities: Dict[str, GraphQLObjectType] = {}
        for field in client.schema.query_type.fields.values():
            if isinstance(field.type, GraphQLObjectType) or isinstance(field.type, GraphQLInterfaceType):
                entities[field.type.name] = field.type
        
        streams = []
        for entity_config in self.config.get('entities'):
            entity = entities[entity_config.get('name')]
            replication_key = entity_config.get('replication_key')
            streams.append(EntityStream(tap=self, entity=entity, replication_key=replication_key, graphql_client=client))

        return streams
