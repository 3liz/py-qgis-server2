""" Abstract class for metrics

    Metric's exporter connectors must
    implement this class.
"""
import json
import os

from abc import ABC, abstractmethod
from dataclasses import dataclass

from pydantic import ConfigDict, Field
from typing_extensions import Dict, Mapping, Optional, Self

from py_qgis_contrib.core import componentmanager as cm
from py_qgis_contrib.core import config

METRICS_HANDLER_ENTRYPOINTS = '3liz.org.map.metrics.handler'
METRICS_HANDLER_CONTRACTID = '@3liz.org/map/metrics/handler;1'


@dataclass(frozen=True)
class Data:
    status: int
    service: str
    request: str
    project: str
    memory_footprint: int
    response_time: int
    latency: int
    cached: bool

    def dump_json(self) -> str:
        return json.dumps(self.__dict__)


class Metrics(ABC):

    @abstractmethod
    async def initialize(**options) -> Self:
        ...

    @abstractmethod
    async def emit(self, key: str, data: Data) -> None:
        ...

#
# Model for arbitrary Metric configuration
#


class MetricConfig(config.Config):
    """ Metric configuration
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str = Field(title="Metric type")
    meta_key: bool = Field(default=False, title="Meta key")
    routing_key: str = Field(
        title="Routing key",
        description=(
            "The routing key for the metric message\n"
            "This key is passed to monitoring backend.\n"
            "If meta_key is true, the string is interpreted as a format string\n"
            "with a 'META' dict parameter."
        ),
        examples=['{META[field1]}.{META[field2]}'],
    )
    routing_key_default: Optional[str] = Field(
        default=None,
        title="Default routing key",
    )
    options: dict = Field(title="Backend configuration options")

    def routing_key_meta(self, meta: Dict[str, str], headers: Mapping[str, str]) -> str:
        """ Returns the routing_key.
            Performs the meta interpolation if needed.
        """
        try:
            return self.routing_key.format(
                META=meta,
                HDRS=headers,
                ENV=os.environ,
            ) if self.meta_key else self.routing_key
        except KeyError:
            return self.routing_key_default

    async def load_service(self) -> Metrics:
        """ Load entrypoint for metrics handler given by 'name'

            raises: cm.FactoryNotFoundError|cm.EntryPointNotFoundError
        """
        cm.load_entrypoint(METRICS_HANDLER_ENTRYPOINTS, self.name)

        # Initialize the service
        return await cm.get_service(
            f"{METRICS_HANDLER_CONTRACTID}?name={self.name}"
        ).initialize(**self.options)
