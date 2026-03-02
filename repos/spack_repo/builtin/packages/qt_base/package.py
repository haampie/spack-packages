import shutil
import sys
import tempfile
from spack_repo.builtin.build_systems.cmake import CMakePackage, generator
from spack.package import *
MACOS_VERSION = macos_version() if sys.platform == "darwin" else None
class QtPackage(CMakePackage):
    """Base package for Qt6 components"""
    homepage = "https://www.qt.io"
    @staticmethod
    def get_url(qualname):
        _url = "https://github.com/qt/{}/archive/refs/tags/v6.2.3.tar.gz"
        return _url.format(qualname.lower())
    @staticmethod
    def get_git(qualname):
        _git = "https://github.com/qt/{}.git"
        return _git.format(qualname.lower())
    @staticmethod
    def get_list_url(qualname):
        _list_url = "https://github.com/qt/{}/tags"
        return _list_url.format(qualname.lower())
        """Remove src/3rdparty libraries that are provided by spack"""
        vendor_dir = join_path(self.stage.source_path, "src", "3rdparty")
        with working_dir(vendor_dir):
            for dep in os.listdir():
                if os.path.isdir(dep):
                    if dep in vendor_deps_to_remove:
                        shutil.rmtree(dep)
class QtBase(QtPackage):
    """Qt Base (Core, Gui, Widgets, Network, ...)"""
    url = QtPackage.get_url(__qualname__)
    list_url = QtPackage.get_list_url(__qualname__)
    variant("gui", default=True, description="Build the Qt GUI module and dependencies.")
    variant("shared", default=True, description="Build shared libraries.")
    variant("sql", default=True, description="Build with SQL support.")
    variant("network", default=False, description="Build with SSL support.")
    # GUI-only dependencies
    variant(
        "accessibility",
        default=False,
        when="+gui",
        description="Build with accessibility support.",
    )
    variant("gtk", default=False, when="+gui", description="Build with gtkplus.")
    variant("opengl", default=False, when="+gui", description="Build with OpenGL support.")
    variant("widgets", default=True, when="+gui", description="Build with widgets.")
    # Dependencies, then variant- and version-specific dependencies
    with when("platform=linux"):
        depends_on("libdrm")
