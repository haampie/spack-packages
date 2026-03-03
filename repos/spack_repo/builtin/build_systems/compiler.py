import pathlib
from typing import Dict, List, Optional, Sequence, Tuple, Union
from spack.package import (
    PackageBase,
)
class CompilerPackage(PackageBase):
    """A Package mixin for all common logic for packages that implement compilers"""
    # TODO: how do these play nicely with other tags
    tags: Sequence[str] = ["compiler"]
    #: Optional suffix regexes for searching for this type of compiler.
    #: Flag used to get verbose output
    verbose_flags: str = "-v"
    #: Flag to activate OpenMP support
    @property
    def cc(self) -> Optional[str]:
        assert self.spec.concrete, "cannot retrieve C compiler, spec is not concrete"
        if self.spec.external:
            return self.spec.extra_attributes.get("compilers", {}).get("c", None)
