"""GraphQL client handling, including TheGraphStream base class."""

import json
import subprocess

from singer_sdk.streams import GraphQLStream
from functools import cached_property


class SubgraphStream(GraphQLStream):
    api_json_schema: dict
    subgraph_url: str
    subgraph_name: str

    def __init__(self, *args, **kwargs):
        self.subgraph_url = kwargs.pop('subgraph_url')
        self.subgraph_name = self.subgraph_url.split('/')[-1]
        self.api_json_schema = json.loads(
            subprocess.run(['graphql-api-to-json-schema', self.subgraph_url],
                           stdout=subprocess.PIPE).stdout.decode('utf-8'))

        super().__init__(*args, **kwargs)

    @cached_property
    def url_base(self) -> str:
        return self.subgraph_url
