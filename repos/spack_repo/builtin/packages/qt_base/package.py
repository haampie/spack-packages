import shutil
import sys
import tempfile
from spack_repo.builtin.build_systems.cmake import CMakePackage, generator
from spack.package import *
MACOS_VERSION = macos_version() if sys.platform == "darwin" else None
class QtPackage(CMakePackage):
    """Base package for Qt6 components"""
    homepage = "https://www.qt.io"
    def get_list_url(qualname):
        _list_url = "https://github.com/qt/{}/tags"
        return _list_url.format(qualname.lower())
class QtBase(QtPackage):
    """Qt Base (Core, Gui, Widgets, Network, ...)"""
