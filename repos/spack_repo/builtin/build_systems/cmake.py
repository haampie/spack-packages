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
def _conditional_cmake_defaults(pkg: PackageBase, args: List[str]) -> None:
    """Set a few default defines for CMake, depending on its version."""
    cmakes = pkg.spec.dependencies("cmake", deptype="build")
    if len(cmakes) != 1:
        return
    cmake = cmakes[0]
    # CMAKE_INTERPROCEDURAL_OPTIMIZATION only exists for CMake >= 3.9
    try:
        ipo = pkg.spec.variants["ipo"].value
    except KeyError:
        ipo = False
    if cmake.satisfies("@3.9:"):
        args.append(define("CMAKE_INTERPROCEDURAL_OPTIMIZATION", ipo))
    # Disable Package Registry: export(PACKAGE) may put files in the user's home directory, and
    # find_package may search there. This is not what we want.
    # Do not populate CMake User Package Registry
    if cmake.satisfies("@3.15:"):
        # see https://cmake.org/cmake/help/latest/policy/CMP0090.html
        args.append(define("CMAKE_POLICY_DEFAULT_CMP0090", "NEW"))
    elif cmake.satisfies("@3.1:"):
        # see https://cmake.org/cmake/help/latest/variable/CMAKE_EXPORT_NO_PACKAGE_REGISTRY.html
        args.append(define("CMAKE_EXPORT_NO_PACKAGE_REGISTRY", True))
    # Do not use CMake User/System Package Registry
    # https://cmake.org/cmake/help/latest/manual/cmake-packages.7.html#disabling-the-package-registry
    if cmake.satisfies("@3.16:"):
        args.append(define("Boost_NO_BOOST_CMAKE", True))
def generator(*names: str, default: Optional[str] = None) -> None:
    """The build system generator to use.
    See ``cmake --help`` for a list of valid generators.
    Currently, "Unix Makefiles" and "Ninja" are the only generators
    that Spack supports. Defaults to "Unix Makefiles".
    See https://cmake.org/cmake/help/latest/manual/cmake-generators.7.html
    for more information.
    Args:
        names: allowed generators for this package
        default: default generator
    """
    allowed_values = ("make", "ninja")
    if any(x not in allowed_values for x in names):
        msg = "only 'make' and 'ninja' are allowed for CMake's 'generator' directive"
        raise ValueError(msg)
    default = default or names[0]
    not_used = [x for x in allowed_values if x not in names]
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
    disable_cmake_hints_from: List[str] = []
    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = "CMakePackage"
    #: Legacy buildsystem attribute used to deserialize and install old specs
        #
        # Currently in Spack msvc is modeled as both the fortran/cxx compiler
