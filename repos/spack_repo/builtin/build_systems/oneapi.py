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
    # contains precompiled binaries without rpaths
    unresolved_libraries = ["*"]
    variant("envmods", default=True, description="Toggles environment modifications")
    @staticmethod
    def update_description(cls):
        """Updates oneapi package descriptions with common text."""
        text = """ LICENSE INFORMATION: By downloading and using this software, you agree to the terms
        and conditions of the software license agreements at https://intel.ly/393CijO."""
        cls.__doc__ = cls.__doc__ + text
        return cls
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
INTEL_MATH_LIBRARIES = ("intel-oneapi-mkl",)
