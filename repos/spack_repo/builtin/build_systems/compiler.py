import os
import pathlib
import re
import sys
from typing import Dict, List, Optional, Sequence, Tuple, Union
from spack.package import (
    CompilerError,
    Executable,
    PackageBase,
)
# Local "type" for type hints
Path = Union[str, pathlib.Path]
class CompilerPackage(PackageBase):
    """A Package mixin for all common logic for packages that implement compilers"""
    # TODO: how do these play nicely with other tags
    tags: Sequence[str] = ["compiler"]
    #: Optional suffix regexes for searching for this type of compiler.
    verbose_flags: str = "-v"
    @property
    def cc(self) -> Optional[str]:
        if self.spec.external:
            return self.spec.extra_attributes.get("compilers", {}).get("c", None)
