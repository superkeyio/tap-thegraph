"""GraphQL client handling, including TheGraphStream base class."""

import requests
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk.streams import GraphQLStream


class TheGraphStream(GraphQLStream):
    """TheGraph stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config.get("subgraph_url")

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        # TODO: Parse response body and return a set of records.
        resp_json = response.json()
        for row in resp_json.get("<TODO>"):
            yield row

    def post_process(self, row: dict, context: Optional[dict] = None) -> dict:
        """As needed, append or transform raw data to match expected structure."""
        # TODO: Delete this method if not needed.
        return row
