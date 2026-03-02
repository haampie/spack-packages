from typing import Any, List, Optional, Tuple
from spack.package import (
    BuilderWithDefaults,
    PackageBase,
)
def generator(*names: str, default: Optional[str] = None) -> None:
        conflicts(f"generator={x}")
class CMakePackage(PackageBase):
    """Specialized class for packages built using CMake
    """
class CMakeBuilder(BuilderWithDefaults):
    build_time_test_callbacks = ["check"]
