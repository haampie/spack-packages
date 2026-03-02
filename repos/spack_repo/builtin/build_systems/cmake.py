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
    default_buildsystem = "cmake"
    build_system("cmake")
    with when("build_system=cmake"):
        # https://cmake.org/cmake/help/latest/variable/CMAKE_BUILD_TYPE.html
        # See https://github.com/spack/spack/pull/36679 and related issues for a
        # discussion of the trade-offs between Release and RelWithDebInfo for default
        # builds. Release is chosen to maximize performance and reduce disk-space burden,
        # at the cost of more difficulty in debugging.
        variant(
            "build_type",
            default="Release",
            description="CMake build type",
            values=("Debug", "Release", "RelWithDebInfo", "MinSizeRel"),
        )
        # CMAKE_INTERPROCEDURAL_OPTIMIZATION only exists for CMake >= 3.9
        # https://cmake.org/cmake/help/latest/variable/CMAKE_INTERPROCEDURAL_OPTIMIZATION.html
        variant(
            "ipo",
            default=False,
            when="^cmake@3.9:",
            description="CMake interprocedural optimization",
        )
        if sys.platform == "win32":
            generator("ninja")
        else:
            generator("ninja", "make", default="make")
        # CMake earlier than 4.1 improperly handles arguments provided to
        # the linker when using msvc as a c/cxx compiler and oneapi as a
        # fortran compiler https://gitlab.kitware.com/cmake/cmake/-/issues/26005
        #
        # Currently in Spack msvc is modeled as both the fortran/cxx compiler
        # due to restrictions w/ oneapi on Windows, but in reality, when msvc
        # is the fortran compiler, it is utilizing oneapi, and this
        # must conflict.
        # this should be updated to reflect a oneapi fortran provider
        # once oneapi is usable with fortran on Windows
        # NOTE: commented out for now because cmake@3 is used in Spack CI
        # successfully with %fortran=msvc.
        # depends_on("cmake@4.1:", type="build", when="%cxx=msvc %fortran=msvc")
    # Legacy methods (used by too many packages to change them,
    # need to forward to the builder)
@register_builder("cmake")
class CMakeBuilder(BuilderWithDefaults):
    """The cmake builder encodes the default way of building software with CMake. IT
    has three phases that can be overridden:
        1. :py:meth:`~.CMakeBuilder.cmake`
        2. :py:meth:`~.CMakeBuilder.build`
        3. :py:meth:`~.CMakeBuilder.install`
    They all have sensible defaults and for many packages the only thing
    necessary will be to override :py:meth:`~.CMakeBuilder.cmake_args`.
    For a finer tuning you may also override:
        +-----------------------------------------------+--------------------+
        | **Method**                                    | **Purpose**        |
        +===============================================+====================+
        | :py:meth:`~.CMakeBuilder.root_cmakelists_dir` | Location of the    |
        |                                               | root CMakeLists.txt|
        +-----------------------------------------------+--------------------+
        | :py:meth:`~.CMakeBuilder.build_directory`     | Directory where to |
        |                                               | build the package  |
        +-----------------------------------------------+--------------------+
    """
    #: Phases of a CMake package
    phases: Tuple[str, ...] = ("cmake", "build", "install")
    #: Names associated with package methods in the old build-system format
    package_methods: Tuple[str, ...] = ("cmake_args", "check")
    #: Names associated with package attributes in the old build-system format
    package_attributes: Tuple[str, ...] = (
        "build_targets",
        "install_targets",
        "build_time_test_callbacks",
        "archive_files",
        "root_cmakelists_dir",
        "std_cmake_args",
        "build_dirname",
        "build_directory",
    )
    #: Targets to be used during the build phase
    build_targets: List[str] = []
    #: Targets to be used during the install phase
    install_targets = ["install"]
    #: Callback names for build-time test
    build_time_test_callbacks = ["check"]
