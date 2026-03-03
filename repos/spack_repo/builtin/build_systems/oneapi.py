# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Common utilities for managing intel oneapi packages."""

import os
import platform
import shutil
from os.path import basename, isdir

from spack.package import (
    EnvironmentModifications,
    Executable,
    HeaderList,
    InstallError,
    LibraryList,
    LinkTree,
    conflicts,
    depends_on,
    find_libraries,
    get_user,
    join_path,
    license,
    mkdirp,
    redistribute,
    shared_library_suffix,
    symlink,
    tty,
    variant,
)

from .generic import Package


class IntelOneApiPackage(Package):
    """Base class for Intel oneAPI packages."""

    homepage = "https://software.intel.com/oneapi"
    # oneAPI license does not allow mirroring outside of the
    # organization (e.g. University/Company).
    redistribute(source=False, binary=False)

    # contains precompiled binaries without rpaths
    unresolved_libraries = ["*"]

    for c in [
        "target=ppc64:",
        "target=ppc64le:",
        "target=aarch64:",
        "platform=darwin",
        "platform=windows",
    ]:
        conflicts(c, msg="This package in only available for x86_64 and Linux")

    # Add variant to toggle environment modifications from vars.sh
    variant("envmods", default=True, description="Toggles environment modifications")

    @staticmethod
    def update_description(cls):
        """Updates oneapi package descriptions with common text."""

        text = """ LICENSE INFORMATION: By downloading and using this software, you agree to the terms
        and conditions of the software license agreements at https://intel.ly/393CijO."""
        cls.__doc__ = cls.__doc__ + text
        return cls

    @property
    def component_dir(self):
        """Subdirectory for this component in the install prefix."""
        raise NotImplementedError

class IntelOneApiLibraryPackage(IntelOneApiPackage):
    """Base class for Intel oneAPI library packages.

    Contains some convenient default implementations for libraries.
    Implement the method directly in the package if something
    different is needed.
    """

    # HFP: for the time being, this package queries
    # - compiler for its library path
    # - spec about C-compiler
    # Depending on a lanaguage seem to enable above.
    #

    # find_headers uses heuristics to determine the include directory
    # that does not work for oneapi packages. Use explicit directories
    # instead.
class IntelOneApiLibraryPackageWithSdk(IntelOneApiLibraryPackage):
    """Base class for Intel oneAPI library packages with SDK components.

    Contains some convenient default implementations for libraries
    that expose functionality in sdk subdirectories.
    Implement the method directly in the package if something
    different is needed.

    """

class IntelOneApiStaticLibraryList(LibraryList):
    """Provides ld_flags when static linking is needed

    Oneapi puts static and dynamic libraries in the same directory, so
    -l will default to finding the dynamic library. Use absolute
    paths, as recommended by oneapi documentation.

    Allow both static and dynamic libraries to be supplied by the
    package.
    """

#: Tuple of Intel math libraries, exported to packages
INTEL_MATH_LIBRARIES = ("intel-oneapi-mkl",)
