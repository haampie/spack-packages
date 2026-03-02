# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.xorg import XorgPackage

from spack.package import *


class Scrnsaverproto(AutotoolsPackage, XorgPackage):
    """MIT Screen Saver Extension.

    This extension defines a protocol to control screensaver features
    and also to query screensaver info on specific windows."""

    homepage = "https://cgit.freedesktop.org/xorg/proto/scrnsaverproto"
    xorg_mirror_path = "proto/scrnsaverproto-1.2.2.tar.gz"

    license("X11")



