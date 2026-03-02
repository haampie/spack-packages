import re
from typing import Any, List, Optional, Tuple
from spack.package import (
    BuilderWithDefaults,
    PackageBase,
)
def generator(*names: str, default: Optional[str] = None) -> None:
    def _values(x):
        return x in allowed_values
        conflicts(f"generator={x}")
class CMakePackage(PackageBase):
    """Specialized class for packages built using CMake
    For more information on the CMake build system, see:
    https://cmake.org/cmake/help/latest/
    """
    #: List of package names for which CMake argument injection should be disabled
class CMakeBuilder(BuilderWithDefaults):
    build_time_test_callbacks = ["check"]
