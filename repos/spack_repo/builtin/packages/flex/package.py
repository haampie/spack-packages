from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack.package import *
class Flex(AutotoolsPackage):
    version("2.6.4", sha256="e87aae032bf07c26f85ac0ed3250998c37621d95f8bd748b31f15b33c45ee995")
    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("bison", type="build")
