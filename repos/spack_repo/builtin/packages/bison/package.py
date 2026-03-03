from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.gnu import GNUMirrorPackage
from spack.package import *
class Bison(AutotoolsPackage, GNUMirrorPackage):
    version("3.7.5", sha256="151cb5f12716e3fe93a27a317cd44878329659f275b342779bfaef4a526bbf70")
    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    conflicts(
        "%oneapi",
        msg=(
            "bison is likely miscompiled by oneapi compilers, "
        ),
    )
