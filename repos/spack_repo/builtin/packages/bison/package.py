import re
import sys
from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.gnu import GNUMirrorPackage
from spack.package import *
class Bison(AutotoolsPackage, GNUMirrorPackage):
    """Bison is a general-purpose parser generator that converts
    an annotated context-free grammar into a deterministic LR or
    generalized LR (GLR) parser employing LALR(1) parser tables."""
    homepage = "https://www.gnu.org/software/bison/"
    gnu_mirror_path = "bison/bison-3.6.4.tar.gz"
    tags = ["build-tools"]
    executables = ["^bison$"]
    version("3.7.5", sha256="151cb5f12716e3fe93a27a317cd44878329659f275b342779bfaef4a526bbf70")
    variant("color", default=False, description="Enable experimental colored output", when="@3.4:")
    # https://lists.gnu.org/archive/html/bug-bison/2019-08/msg00008.html
    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    conflicts(
        "%oneapi",
        msg=(
            "bison is likely miscompiled by oneapi compilers, "
            "see https://github.com/spack/spack/issues/37172"
        ),
    )
    build_directory = "spack-build"
