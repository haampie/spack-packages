# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.xorg import XorgPackage

from spack.package import *


class Xvidtune(AutotoolsPackage, XorgPackage):
    """xvidtune is a client interface to the X server video mode
    extension (XFree86-VidModeExtension)."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xvidtune"
    xorg_mirror_path = "app/xvidtune-1.0.3.tar.gz"

    license("MIT")



    depends_on("libxxf86vm")
    depends_on("libxt")
    depends_on("libxaw")
    depends_on("libxmu")
    depends_on("libx11")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
