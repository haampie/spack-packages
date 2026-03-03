from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.compiler import CompilerPackage
from spack_repo.builtin.build_systems.gnu import GNUMirrorPackage
from spack.package import *
class Gcc(AutotoolsPackage, GNUMirrorPackage, CompilerPackage):
    provides("c", "cxx", when="languages=c,c++")
    version("15.2.0", sha256="438fd996826b0c82485a29da03a72d71d6e3541a83ec702df4271f6fe025d24e")
    variant(
        "languages",
        default="c,c++,fortran",
        values=(
            "c",
            "c++",
        ),
        multi=True,
    )
