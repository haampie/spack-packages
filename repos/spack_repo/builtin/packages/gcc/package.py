from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.compiler import CompilerPackage
from spack_repo.builtin.build_systems.gnu import GNUMirrorPackage
from spack.package import *
class Gcc(AutotoolsPackage, GNUMirrorPackage, CompilerPackage):
    provides("c", "cxx", when="languages=c,c++")
    variant(
        "languages",
        default="c,c++,fortran",
        values=(
            "ada",
            "brig",
            "c",
            "c++",
            "d",
            "obj-c++",
        ),
        multi=True,
        description="Compilers and runtime libraries to build",
    )
    variant("nvptx", default=False, description="Target nvptx offloading to NVIDIA GPUs")
    variant("bootstrap", default=True, description="Enable 3-stage bootstrap")
