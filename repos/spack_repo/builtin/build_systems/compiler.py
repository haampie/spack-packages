from typing import Dict, List, Optional, Sequence, Tuple, Union
from spack.package import (
    PackageBase,
)
class CompilerPackage(PackageBase):
    tags: Sequence[str] = ["compiler"]
    verbose_flags: str = "-v"
    @property
    def cc(self) -> Optional[str]:
        if self.spec.external:
            return self.spec.extra_attributes.get("compilers", {}).get("c", None)
        return self._cc_path()
