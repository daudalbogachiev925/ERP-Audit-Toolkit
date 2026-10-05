"""ERP Audit Toolkit — аудит конфигурации 1С:ERP."""

__version__ = "0.1.0"

from erp_audit.parser import MetadataObject, iter_objects, parse_metadata
from erp_audit.graph import build_graph, find_cycles, find_orphans, top_hubs
from erp_audit.metrics import BslMetrics, analyze_bsl_file

__all__ = [
    "__version__",
    "MetadataObject",
    "iter_objects",
    "parse_metadata",
    "build_graph",
    "find_cycles",
    "find_orphans",
    "top_hubs",
    "BslMetrics",
    "analyze_bsl_file",
]
