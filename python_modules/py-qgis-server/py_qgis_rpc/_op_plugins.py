#
# Plugins inspection
#
from py_qgis_contrib.core.qgis import QgisPluginService

from . import messages as _m


def inspect_plugins(
    conn: _m.Connection,
    s: QgisPluginService,
):
    _m.stream_data(
        conn,
        (
            _m.PluginInfo(
                name=p.name,
                path=p.path,
                plugin_type=p.plugin_type.value,
                metadata=p.metadata,
            ) for p in s.plugins
        ),
    )
