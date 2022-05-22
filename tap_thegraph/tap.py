"""TheGraph tap class."""

import logging
from typing import Dict, List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers
# TODO: Import your custom stream types here:
from tap_thegraph.streams import (
    EntityStream, )

EntityType = th.ObjectType(
    th.Property("name", th.StringType, required=True),
    th.Property(
        "replication_key",
        th.StringType,
        description=
        "Name of the field used for incremental replication (i.e. timestamp)"))

SubgraphType = th.ObjectType(
    th.Property(
        "url",
        th.StringType,
        required=True,
    ), th.Property("entities", th.ArrayType(EntityType), required=True))


class TapTheGraph(Tap):
    """TheGraph tap class."""
    name = "tap-thegraph"

    config_jsonschema = th.PropertiesList(
        th.Property("subgraphs", th.ArrayType(SubgraphType),
                    required=True)).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""

        streams = []
        for subgraph_config in self.config.get('subgraphs'):
            for entity_config in subgraph_config.get('entities'):
                streams.append(
                    EntityStream(
                        tap=self,
                        entity_name=entity_config.get('name'),
                        replication_key=entity_config.get('replication_key'),
                        subgraph_url=subgraph_config.get('url')))

        return streams
