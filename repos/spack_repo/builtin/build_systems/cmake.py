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
        args.append(define("CMAKE_FIND_USE_PACKAGE_REGISTRY", False))
    elif cmake.satisfies("@3.1:3.15"):
        args.append(define("CMAKE_FIND_PACKAGE_NO_PACKAGE_REGISTRY", False))
        args.append(define("CMAKE_FIND_PACKAGE_NO_SYSTEM_PACKAGE_REGISTRY", False))
    # Export a compilation database if supported.
    if _supports_compilation_databases(pkg):
        args.append(define("CMAKE_EXPORT_COMPILE_COMMANDS", True))
    # Enable MACOSX_RPATH by default when cmake_minimum_required < 3
    # https://cmake.org/cmake/help/latest/policy/CMP0042.html
    if pkg.spec.satisfies("platform=darwin") and cmake.satisfies("@3:"):
        args.append(define("CMAKE_POLICY_DEFAULT_CMP0042", "NEW"))
    # Disable find package's config mode for versions of Boost that
    # didn't provide it. See https://github.com/spack/spack/issues/20169
    # and https://cmake.org/cmake/help/latest/module/FindBoost.html
    if pkg.spec.satisfies("^boost@:1.69.0"):
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
        # due to restrictions w/ oneapi on Windows, but in reality, when msvc
        # is the fortran compiler, it is utilizing oneapi, and this
        # must conflict.
        # this should be updated to reflect a oneapi fortran provider
        # once oneapi is usable with fortran on Windows
        # NOTE: commented out for now because cmake@3 is used in Spack CI
        # successfully with %fortran=msvc.
        # depends_on("cmake@4.1:", type="build", when="%cxx=msvc %fortran=msvc")
    def flags_to_build_system_args(self, flags):
        """Return a list of all command line arguments to pass the specified
        compiler flags to cmake. Note CMAKE does not have a cppflags option,
        so cppflags will be added to cflags, cxxflags, and fflags to mimic the
        behavior in other tools.
        """
        # Has to be dynamic attribute due to caching
        setattr(self, "cmake_flag_args", [])
        flag_string = "-DCMAKE_{0}_FLAGS={1}"
        langs = {"C": "c", "CXX": "cxx", "Fortran": "f"}
        # Handle language compiler flags
        for lang, pre in langs.items():
            flag = pre + "flags"
            # cmake has no explicit cppflags support -> add it to all langs
            lang_flags = " ".join(flags.get(flag, []) + flags.get("cppflags", []))
            if lang_flags:
                self.cmake_flag_args.append(flag_string.format(lang, lang_flags))
        # Cmake has different linker arguments for different build types.
        # We specify for each of them.
        if flags["ldflags"]:
            ldflags = " ".join(flags["ldflags"])
            # cmake has separate linker arguments for types of builds.
            self.cmake_flag_args.append(f"-DCMAKE_EXE_LINKER_FLAGS={ldflags}")
            self.cmake_flag_args.append(f"-DCMAKE_MODULE_LINKER_FLAGS={ldflags}")
            self.cmake_flag_args.append(f"-DCMAKE_SHARED_LINKER_FLAGS={ldflags}")
        # CMake has libs options separated by language. Apply ours to each.
        if flags["ldlibs"]:
            libs_flags = " ".join(flags["ldlibs"])
    #: Callback names for build-time test
    build_time_test_callbacks = ["check"]
