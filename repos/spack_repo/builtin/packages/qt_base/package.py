from spack_repo.builtin.build_systems.cmake import CMakePackage, generator
from spack.package import *
class QtPackage(CMakePackage):
    vendor_deps_to_remove = []
class QtBase(QtPackage):
    variant("widgets", default=True, when="+gui", description="Build with widgets.")
