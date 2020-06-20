from pbr.version import VersionInfo

__version__ = VersionInfo('hello_gh_actions').version_string()
__version_info__ = VersionInfo('hello_gh_actions').semantic_version().version_tuple()

from .hello import HelloWorld
