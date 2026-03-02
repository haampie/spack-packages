import pathlib
import shutil
import sys
from spack_repo.builtin.build_systems.generic import Package
from spack.package import *
class CompilerWrapper(Package):
    """Spack compiler wrapper script.
    Compiler commands go through this compiler wrapper in Spack builds.
    The compiler wrapper is a thin layer around the standard compilers.
    """
    homepage = "https://github.com/spack/spack"
    url = f"file:///{pathlib.PurePath(__file__).parent}/cc.sh"
    if sys.platform != "win32":
        version(
            "1.0",
        )
