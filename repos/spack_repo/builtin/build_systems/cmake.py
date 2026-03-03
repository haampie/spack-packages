import sys
from typing import Any, List, Optional, Tuple
from spack.package import (
    PackageBase,
    working_dir,
)
# Regex to extract the primary generator from the CMake generator
def _conditional_cmake_defaults(pkg: PackageBase, args: List[str]) -> None:
        return
def generator(*names: str, default: Optional[str] = None) -> None:
    """The build system generator to use.
        names: allowed generators for this package
        default: default generator
    """
    allowed_values = ("make", "ninja")
class CMakePackage(PackageBase):
    """Specialized class for packages built using CMake
    """
