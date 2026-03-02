# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.xorg import XorgPackage

from spack.package import *


class Libxvmc(AutotoolsPackage, XorgPackage):
    """X.org libXvMC library."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libXvMC"
    xorg_mirror_path = "lib/libXvMC-1.0.9.tar.gz"

    license("MIT")

    maintainers("wdconinc")

    version("1.0.10", sha256="d8306f71c798d10409bb181b747c2644e1d60c05773c742c12304ab5aa5c8436")
    version("1.0.9", sha256="090f087fe65b30b3edfb996c79ff6cf299e473fb25e955fff1c4e9cb624da2c2")

    depends_on("c", type="build")

    depends_on("libx11@1.6:")
    depends_on("libxext")
    depends_on("libxv")

    depends_on("xextproto", type=("build", "link"))
    depends_on("videoproto", type=("build", "link"))
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
