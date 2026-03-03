# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.sourceforge import SourceforgePackage

from spack.package import *


class Libexif(AutotoolsPackage, SourceforgePackage):
    """A library to parse an EXIF file and read the data from those tags"""

    homepage = "https://libexif.github.io/"
    url = "https://github.com/libexif/libexif/releases/download/v0.6.24/libexif-0.6.24.tar.bz2"




    depends_on("c", type="build")
    depends_on("glib")

    def url_for_version(self, version):
        if self.spec.satisfies("@:0.6.21"):
            return f"https://downloads.sourceforge.net/project/libexif/libexif/{version}/libexif-{version}.tar.bz2"
        else:
            return f"https://github.com/libexif/libexif/releases/download/v{version}/libexif-{version}.tar.bz2"
