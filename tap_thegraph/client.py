"""GraphQL client handling, including TheGraphStream base class."""

import json
import logging
from pprint import pprint
import subprocess

import jsonref
from gql import Client as GraphQLClient, gql
from gql.transport.requests import RequestsHTTPTransport
from gql.transport.requests import log as requests_logger
from singer_sdk.streams import GraphQLStream

the_graph_builtin_type_to_json_schema_type = {
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
    }
}

# TODO: handle recursion in JSON schema by only showing IDs for other entities
# How do detect entities and modify JSON schema appropriately?
# Is there some library for walking / transforming JSON in Python?


class SubgraphStream(GraphQLStream):
    graphql_client: GraphQLClient
    api_json_schema: dict
    subgraph_url: str
    subgraph_name: str

    def _simplify_json_schema(self, api_json_schema):
        # do some kind of simplification here
        # only do IDs
        return api_json_schema

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

        self.api_json_schema = jsonref.loads(subprocess.run(
            ['subgraph-to-json-schema', self.subgraph_url],
            stdout=subprocess.PIPE).stdout.decode('utf-8'),
                                             jsonschema=True)

        self.api_json_schema = self._simplify_json_schema(self.api_json_schema)
        super().__init__(*args, **kwargs)

    @property
    def url_base(self) -> str:
        return self.subgraph_url
