# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import Optional
from spack.package import PackageBase, join_url
class GNUMirrorPackage(PackageBase):
    """Mixin that takes care of setting url and mirrors for GNU packages."""
    #: Path of the package in a GNU mirror
    gnu_mirror_path: Optional[str] = None
