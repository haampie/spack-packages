import re
import sys
from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.gnu import GNUMirrorPackage
from spack.package import *
class Bison(AutotoolsPackage, GNUMirrorPackage):
    executables = ["^bison$"]
    version("3.6.3", sha256="4b4c4943931e811f1073006ce3d8ee022a02b11b501e9cbf4def3613b24a3e63")
    version("3.6.2", sha256="e28ed3aad934de2d1df68be209ac0b454f7b6d3c3d6d01126e5cd2cbadba089a")
    # https://lists.gnu.org/archive/html/bug-bison/2019-08/msg00008.html
    patch("parallel.patch", when="@3.4.2")
    depends_on("cxx", type="build")  # generated
    depends_on("m4@1.4.6:", type=("build", "run"))
    conflicts(
        "%oneapi",
        msg=(
            "bison is likely miscompiled by oneapi compilers, "
        ),
    )
