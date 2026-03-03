# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from typing import Optional

from spack.package import PackageBase, join_url


class XorgPackage(PackageBase):
    """Mixin that takes care of setting url and mirrors for x.org
    packages."""

    #: Path of the package in a x.org mirror
    xorg_mirror_path: Optional[str] = None

    #: List of x.org mirrors used by Spack
    #  Note: x.org mirrors are a bit tricky, since many are out-of-sync or off.
    #        A good package to test with is `util-macros`, which had a "recent"
    #        release.
    base_mirrors = [
        "https://www.x.org/archive/individual/",
        "https://mirrors.ircam.fr/pub/x.org/individual/",
        "https://mirror.transip.net/xorg/individual/",
        "ftp://ftp.freedesktop.org/pub/xorg/individual/",
        "http://xorg.mirrors.pair.com/individual/",
    ]

