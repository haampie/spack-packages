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
