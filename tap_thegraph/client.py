"""GraphQL client handling, including TheGraphStream base class."""

import logging
import subprocess
from typing import Iterable, Optional

import jsonref
import requests
from gql import Client as GraphQLClient, gql
from gql.transport.requests import RequestsHTTPTransport
from gql.transport.requests import log as requests_logger
from singer_sdk.streams import GraphQLStream


class SubgraphStream(GraphQLStream):
    """TheGraph stream class."""

    graphql_client: GraphQLClient
    api_json_schema: dict
    subgraph_url: str
    subgraph_name: str

    def __init__(self, *args, **kwargs):
        requests_logger.setLevel(logging.WARNING)
        self.subgraph_url = kwargs.pop('subgraph_url')
        self.subgraph_name = self.subgraph_url.split('/')[-1]
        transport = RequestsHTTPTransport(
            url=self.subgraph_url,
            verify=True,
            retries=3,
        )
        self.graphql_client = GraphQLClient(transport=transport,
                                            fetch_schema_from_transport=True)

        noop_query = """
        {
            __schema {
                queryType {
                    name
                }
            }
        }
        """
        self.graphql_client.execute(gql(noop_query))

        self.api_json_schema = jsonref.loads(
            subprocess.run(['subgraph-to-json-schema', self.subgraph_url],
                           stdout=subprocess.PIPE).stdout.decode('utf-8'))
        super().__init__(*args, **kwargs)

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.subgraph_url

    def post_process(self, row: dict, context: Optional[dict] = None) -> dict:
        """As needed, append or transform raw data to match expected structure."""
        # TODO: Delete this method if not needed.
        return row
