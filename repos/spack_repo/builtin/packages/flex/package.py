from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack.package import *
class Flex(AutotoolsPackage):
    version("2.6.0", sha256="cde6e46064a941a3810f7bbc612a2c39cb3aa29ce7eb775089c2515d0adfa7e9")
    depends_on("cxx", type="build")  # generated
    depends_on("bison", type="build")
