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
    #: version suffix for gcc.
    compiler_suffixes: List[str] = [r"-.*"]

    #: Optional prefix regexes for searching for this compiler
    compiler_prefixes: List[str] = []

    #: Compiler argument(s) that produces version information
    #: If multiple arguments, the earlier arguments must produce errors when invalid
    compiler_version_argument: Union[str, Tuple[str, ...]] = "-dumpversion"

    #: Regex used to extract version from compiler's output
    compiler_version_regex: str = "(.*)"

    #: Static definition of languages supported by this class
    compiler_languages: Sequence[str] = ["c", "cxx", "fortran"]

    #: Relative path to compiler wrappers
    compiler_wrapper_link_paths: Dict[str, str] = {}

    #: Optimization flags
    opt_flags: Sequence[str] = []
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

    def archspec_name(self) -> str:
        """Name that archspec uses to refer to this compiler"""
        return self.spec.name

    @property
    def cc(self) -> Optional[str]:
        assert self.spec.concrete, "cannot retrieve C compiler, spec is not concrete"
        if self.spec.external:
            return self.spec.extra_attributes.get("compilers", {}).get("c", None)
        return self._cc_path()

    def _cc_path(self) -> Optional[str]:
        """Returns the path to the C compiler, if the package was installed by Spack"""
        return None

    @property
    def cxx(self) -> Optional[str]:
        assert self.spec.concrete, "cannot retrieve C++ compiler, spec is not concrete"
        if self.spec.external:
            return self.spec.extra_attributes.get("compilers", {}).get("cxx", None)
        return self._cxx_path()

    def _cxx_path(self) -> Optional[str]:
        """Returns the path to the C++ compiler, if the package was installed by Spack"""
        return None

    @property
    def fortran(self):
        assert self.spec.concrete, "cannot retrieve Fortran compiler, spec is not concrete"
        if self.spec.external:
            return self.spec.extra_attributes.get("compilers", {}).get("fortran", None)
        return self._fortran_path()

    def _fortran_path(self) -> Optional[str]:
        """Returns the path to the Fortran compiler, if the package was installed by Spack"""
        return None


@memoized
def _compiler_output(
    compiler_path: Path, *, version_argument: str, ignore_errors: Tuple[int, ...] = ()
) -> str:
    """Returns the output from the compiler invoked with the given version argument.

    Args:
        compiler_path: path of the compiler to be invoked
        version_argument: the argument used to extract version information
    """
    compiler = Executable(compiler_path)
    if not version_argument:
        return compiler(
            output=str, error=str, ignore_errors=ignore_errors, timeout=120, fail_on_error=True
        )
    return compiler(
        version_argument,
        output=str,
        error=str,
        ignore_errors=ignore_errors,
        timeout=120,
        fail_on_error=True,
    )


def compiler_output(
    compiler_path: Path, *, version_argument: str, ignore_errors: Tuple[int, ...] = ()
) -> str:
    """Wrapper for _get_compiler_version_output()."""
    # This ensures that we memoize compiler output by *absolute path*,
    # not just executable name. If we don't do this, and the path changes
    # (e.g., during testing), we can get incorrect results.
    if not os.path.isabs(compiler_path):
        compiler_path = which_string(str(compiler_path), required=True)

    return _compiler_output(
        compiler_path, version_argument=version_argument, ignore_errors=ignore_errors
    )
