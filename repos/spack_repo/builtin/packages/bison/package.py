from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.gnu import GNUMirrorPackage
from spack.package import *
class Bison(AutotoolsPackage, GNUMirrorPackage):
    version("3.6.3", sha256="4b4c4943931e811f1073006ce3d8ee022a02b11b501e9cbf4def3613b24a3e63")
    depends_on("cxx", type="build")  # generated
    depends_on("m4@1.4.6:", type=("build", "run"))
    conflicts(
        "%oneapi",
        msg=(
            "bison is likely miscompiled by oneapi compilers, "
        ),
    )
