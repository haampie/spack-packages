from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack.package import *
class Flex(AutotoolsPackage):
    version("2.6.1", sha256="3c43f9e658e45e8aae3cf69fa11803d60550865f023852830d557c5f0623c13b")
    depends_on("c", type="build")  # generated
    depends_on("bison", type="build")
