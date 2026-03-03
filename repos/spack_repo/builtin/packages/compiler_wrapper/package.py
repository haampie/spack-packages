import pathlib
import shutil
import sys
from spack_repo.builtin.build_systems.generic import Package
from spack.package import *
class CompilerWrapper(Package):
    if sys.platform != "win32":
        version(
            "1.0",
        )
    else:
        version("1.0")
        has_code = False
