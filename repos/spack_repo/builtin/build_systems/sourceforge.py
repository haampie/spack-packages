# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from typing import Optional

from spack.package import PackageBase, join_url


class SourceforgePackage(PackageBase):
    """Mixin that takes care of setting url and mirrors for Sourceforge
    packages."""

    #: Path of the package in a Sourceforge mirror
    sourceforge_mirror_path: Optional[str] = None

    #: List of Sourceforge mirrors used by Spack
    base_mirrors = [
        "https://prdownloads.sourceforge.net/",
        "https://freefr.dl.sourceforge.net/",
        "https://netcologne.dl.sourceforge.net/",
        "https://pilotfiber.dl.sourceforge.net/",
        "https://downloads.sourceforge.net/",
        "http://kent.dl.sourceforge.net/sourceforge/",
    ]

