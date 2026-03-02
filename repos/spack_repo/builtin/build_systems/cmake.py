import re
import sys
from typing import Any, List, Optional, Tuple
from spack.package import (
    BuilderWithDefaults,
    InstallError,
    PackageBase,
    Prefix,
    Spec,
    when,
    working_dir,
)
_primary_generator_extractor = re.compile(r"(?:.* - )?(.*)")
def generator(*names: str, default: Optional[str] = None) -> None:
    def _values(x):
        return x in allowed_values
    for x in not_used:
        conflicts(f"generator={x}")
class CMakePackage(PackageBase):
    """Specialized class for packages built using CMake
    """
class CMakeBuilder(BuilderWithDefaults):
    build_time_test_callbacks = ["check"]
