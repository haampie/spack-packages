from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack.package import *
class Flex(AutotoolsPackage):
    version("2.5.39", sha256="258d3c9c38cae05932fb470db58b6a288a361c448399e6bda2694ef72a76e7cd")
    depends_on("cxx", type="build")  # generated
    depends_on("bison", type="build")
