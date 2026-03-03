import sys
from spack.package import *
class CompilerWrapper(Package):
    if sys.platform != "win32":
        version(
            "1.0",
        )
