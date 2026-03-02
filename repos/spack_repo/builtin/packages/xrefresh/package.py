# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.xorg import XorgPackage

from spack.package import *


class Xrefresh(AutotoolsPackage, XorgPackage):
    """xrefresh - refresh all or part of an X screen."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xrefresh"
    xorg_mirror_path = "app/xrefresh-1.0.5.tar.gz"

    license("MIT")

    version("1.1.0", sha256="cbf0d3ed80f03188841a96ceb20e615b40a006e3928be2e179d9d5a0ded639b2")


    depends_on("libx11")

    depends_on("xproto@7.0.17:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
