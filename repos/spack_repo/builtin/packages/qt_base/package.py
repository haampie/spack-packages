from spack_repo.builtin.build_systems.cmake import CMakePackage, generator
from spack.package import *
class QtPackage(CMakePackage):
        _url = "https://github.com/qt/{}/archive/refs/tags/v6.2.3.tar.gz"
class QtBase(QtPackage):
    variant("shared", default=True, description="Build shared libraries.")
