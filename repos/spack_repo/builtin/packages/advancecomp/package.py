# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Advancecomp(AutotoolsPackage):
    """AdvanceCOMP contains recompression utilities for your .zip archives,
    .png images, .mng video clips and .gz files."""

    homepage = "https://www.advancemame.it"
    url = "https://github.com/amadvance/advancecomp/archive/v2.1.tar.gz"

    license("GPL-3.0-or-later")

    version("2.6", sha256="799397b10d087d0147d6af117a5a473120f1369f0a3a3d68bf953abc0b749b75")
    version("1.22", sha256="b8c482027a5f78d9a7f871cbba19cc896ed61653d1d93034c9dbe55484952605")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("zlib-api", type="link")
