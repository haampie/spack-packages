# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import Optional

from spack.package import PackageBase, join_url


class SourcewarePackage(PackageBase):
    """Mixin that takes care of setting url and mirrors for Sourceware.org
    packages."""

    #: Path of the package in a Sourceware mirror
    sourceware_mirror_path: Optional[str] = None

    #: List of Sourceware mirrors used by Spack
    base_mirrors = [
        "https://sourceware.org/pub/",
        "https://mirrors.kernel.org/sourceware/",
        "https://ftp.gwdg.de/pub/linux/sources.redhat.com/",
    ]

