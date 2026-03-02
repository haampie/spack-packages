# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections.abc
import os
import pathlib
import platform
import re
import sys
from typing import Any, List, Optional, Tuple
from spack.package import (
    BuilderWithDefaults,
    InstallError,
    PackageBase,
    Prefix,
    Spec,
    build_system,
    conflicts,
    depends_on,
    get_cmake_prefix_path,
    register_builder,
    run_after,
    tty,
    variant,
    when,
    working_dir,
)
from ._checks import execute_build_time_tests
# Regex to extract the primary generator from the CMake generator
# string.
_primary_generator_extractor = re.compile(r"(?:.* - )?(.*)")
def generator(*names: str, default: Optional[str] = None) -> None:
    def _values(x):
        return x in allowed_values
    _values.__doc__ = f"{','.join(names)}"
    variant(
        "generator",
        default=default,
        values=_values,
        description="the build system generator to use",
        when="build_system=cmake",
    )
    for x in not_used:
        conflicts(f"generator={x}")
class CMakePackage(PackageBase):
    """Specialized class for packages built using CMake
    For more information on the CMake build system, see:
    https://cmake.org/cmake/help/latest/
    """
    #: List of package names for which CMake argument injection should be disabled
class CMakeBuilder(BuilderWithDefaults):
    build_time_test_callbacks = ["check"]
