from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.compiler import CompilerPackage
from spack_repo.builtin.build_systems.gnu import GNUMirrorPackage
from spack.package import *
class Gcc(AutotoolsPackage, GNUMirrorPackage, CompilerPackage):
    list_url = "https://ftp.gnu.org/gnu/gcc/"
    list_depth = 1
    keep_werror = "all"
    provides("c", "cxx", when="languages=c,c++")
    provides("c", when="languages=c")
    version("master", branch="master")
    # Latest stable
    version("15.2.0", sha256="438fd996826b0c82485a29da03a72d71d6e3541a83ec702df4271f6fe025d24e")
    # Previous stable series releases
    # Final releases of previous versions
    # Deprecated older non-final releases
    with default_args(deprecated=True):
        version("4.8.4", sha256="4a80aa23798b8e9b5793494b8c976b39b8d9aa2e53cd5ed5534aff662a7f8695")
    variant(
        "languages",
        default="c,c++,fortran",
        values=(
            "ada",
            "brig",
            "c",
            "c++",
            "d",
            "fortran",
            "go",
            "java",
            "jit",
            "lto",
            "objc",
            "obj-c++",
        ),
        multi=True,
        description="Compilers and runtime libraries to build",
    )
