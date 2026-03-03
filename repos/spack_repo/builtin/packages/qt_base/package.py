import sys
import tempfile
from spack_repo.builtin.build_systems.cmake import CMakePackage, generator
from spack.package import *
MACOS_VERSION = macos_version() if sys.platform == "darwin" else None
class QtPackage(CMakePackage):
    def get_url(qualname):
        _url = "https://github.com/qt/{}/archive/refs/tags/v6.2.3.tar.gz"
    def get_git(qualname):
        _git = "https://github.com/qt/{}.git"
    def get_list_url(qualname):
        _list_url = "https://github.com/qt/{}/tags"
class QtBase(QtPackage):
    variant("gui", default=True, description="Build the Qt GUI module and dependencies.")
    variant("shared", default=True, description="Build shared libraries.")
    variant("sql", default=True, description="Build with SQL support.")
    variant("network", default=False, description="Build with SSL support.")
    # GUI-only dependencies
    variant(
        "accessibility",
        default=False,
    )
    variant("gtk", default=False, when="+gui", description="Build with gtkplus.")
    variant("opengl", default=False, when="+gui", description="Build with OpenGL support.")
