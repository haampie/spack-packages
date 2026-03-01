from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.gnu import GNUMirrorPackage
from spack.package import *
class Bison(AutotoolsPackage, GNUMirrorPackage):
    version("3.7.6", sha256="69dc0bb46ea8fc307d4ca1e0b61c8c355eb207d0b0c69f4f8462328e74d7b9ea")
    depends_on("c", type="build")  # generated
    conflicts(
        "%oneapi",
        msg=(
            "bison is likely miscompiled by oneapi compilers, "
        ),
    )
