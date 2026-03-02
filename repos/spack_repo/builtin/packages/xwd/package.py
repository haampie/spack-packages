# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.xorg import XorgPackage

from spack.package import *


class Xwd(AutotoolsPackage, XorgPackage):
    """xwd - dump an image of an X window."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xwd"
    xorg_mirror_path = "app/xwd-1.0.6.tar.gz"




    depends_on("libx11")
    depends_on("libxkbfile")

    depends_on("xproto@7.0.17:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
