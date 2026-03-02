from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.gnu import GNUMirrorPackage
from spack.package import *
class Bison(AutotoolsPackage, GNUMirrorPackage):
    version("3.4.2", sha256="ff3922af377d514eca302a6662d470e857bd1a591e96a2050500df5a9d59facf")
    depends_on("c", type="build")  # generated
    depends_on("m4@1.4.6:", type=("build", "run"))
    conflicts(
        "%oneapi",
        msg=(
            "bison is likely miscompiled by oneapi compilers, "
        ),
    )
