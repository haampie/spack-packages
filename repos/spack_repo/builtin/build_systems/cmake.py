import re
import sys
from typing import Any, List, Optional, Tuple
from spack.package import (
    PackageBase,
    working_dir,
)
from ._checks import execute_build_time_tests
# Regex to extract the primary generator from the CMake generator
def _conditional_cmake_defaults(pkg: PackageBase, args: List[str]) -> None:
    """Set a few default defines for CMake, depending on its version."""
    cmakes = pkg.spec.dependencies("cmake", deptype="build")
    if len(cmakes) != 1:
        return
def generator(*names: str, default: Optional[str] = None) -> None:
    """The build system generator to use.
        names: allowed generators for this package
        default: default generator
    """
    allowed_values = ("make", "ninja")
    if any(x not in allowed_values for x in names):
        msg = "only 'make' and 'ninja' are allowed for CMake's 'generator' directive"
class CMakePackage(PackageBase):
    """Specialized class for packages built using CMake
    """
