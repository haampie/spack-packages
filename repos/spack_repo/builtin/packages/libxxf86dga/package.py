# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.xorg import XorgPackage

from spack.package import *


class Libxxf86dga(AutotoolsPackage, XorgPackage):
    """libXxf86dga - Client library for the XFree86-DGA extension."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libXxf86dga"
    xorg_mirror_path = "lib/libXxf86dga-1.1.4.tar.gz"



    version("1.1.4", sha256="e6361620a15ceba666901ca8423e8be0c6ed0271a7088742009160349173766b")



