# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import itertools
import os
import pathlib
import re
import sys
from typing import Dict, List, Optional, Sequence, Tuple, Union
from spack.package import (
    CompilerError,
    Executable,
    PackageBase,
    ProcessError,
    Spec,
    classproperty,
    memoized,
    tty,
    which_string,
)
# Local "type" for type hints
Path = Union[str, pathlib.Path]
class CompilerPackage(PackageBase):
    """A Package mixin for all common logic for packages that implement compilers"""
    # TODO: how do these play nicely with other tags
    tags: Sequence[str] = ["compiler"]
    #: Optional suffix regexes for searching for this type of compiler.
    #: Suffixes are used by some frameworks, e.g. macports uses an '-mp-X.Y'
    #: Flags for generating debug information
    debug_flags: Sequence[str] = []
    #: Returns the argument needed to set the RPATH, or None if it does not exist
    rpath_arg: Optional[str] = "-Wl,-rpath,"
    #: Flag that needs to be used to pass an argument to the linker
    linker_arg: str = "-Wl,"
    #: Flag used to produce Position Independent Code
    pic_flag: str = "-fPIC"
    #: Flag used to get verbose output
    verbose_flags: str = "-v"
    #: Flag to activate OpenMP support
    openmp_flag: str = "-fopenmp"
    implicit_rpath_libs: List[str] = []
    @property
    def cc(self) -> Optional[str]:
        assert self.spec.concrete, "cannot retrieve C compiler, spec is not concrete"
        if self.spec.external:
            return self.spec.extra_attributes.get("compilers", {}).get("c", None)
        return self._cc_path()
    def _cc_path(self) -> Optional[str]:
        """Returns the path to the C compiler, if the package was installed by Spack"""
        return None
