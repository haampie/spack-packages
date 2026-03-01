from typing import Any, List, Optional, Tuple
from spack.package import (
    PackageBase,
)
def generator(*names: str, default: Optional[str] = None) -> None:
    """The build system generator to use.
    """
class CMakePackage(PackageBase):
    """Specialized class for packages built using CMake
    """
