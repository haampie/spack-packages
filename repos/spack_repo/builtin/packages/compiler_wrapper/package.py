import pathlib
import sys
from spack.package import *
class CompilerWrapper(Package):
    """Spack compiler wrapper script.
    """
    if sys.platform != "win32":
        version(
            "1.0",
            sha256="c7b816479554fd32f677db15ceec6627b91c86074a5d65498688afcbe2796188",
            expand=False,
        )
