from pbr.version import VersionInfo

__version__ = VersionInfo('hetzner_fix_report').version_string()
__version_info__ = VersionInfo('hetzner_fix_report').semantic_version().version_tuple()

from .hetzner_fix_report import hetzner_fix_report
