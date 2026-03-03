import sys
from typing import Any, List, Optional, Tuple
from spack.package import (
    PackageBase,
    working_dir,
)
# Regex to extract the primary generator from the CMake generator
def generator(*names: str, default: Optional[str] = None) -> None:
    """The build system generator to use.
    """
    allowed_values = ("make", "ninja")
class CMakePackage(PackageBase):
    """Specialized class for packages built using CMake
    """
