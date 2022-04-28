"""TheGraph tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers
# TODO: Import your custom stream types here:
from tap_thegraph.streams import (
    TheGraphStream,
    EntityStream,
)
from graphql import get_introspection_query, graphql_sync
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

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
        print(client.schema.query_type.fields)
        # for entity in client.schema:
        #     print(entity)


        return []
