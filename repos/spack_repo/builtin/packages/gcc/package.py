from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.compiler import CompilerPackage
from spack_repo.builtin.build_systems.gnu import GNUMirrorPackage
from spack.package import *
class Gcc(AutotoolsPackage, GNUMirrorPackage, CompilerPackage):
    provides("c", "cxx", when="languages=c,c++")
    # Previous stable series releases
    # Final releases of previous versions
    variant(
        "languages",
        default="c,c++,fortran",
        values=(
            "c",
            "c++",
        ),
        multi=True,
    )
    variant("bootstrap", default=True, description="Enable 3-stage bootstrap")
