# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob

from spack_repo.builtin.build_systems.generic import Package
from spack_repo.builtin.build_systems.sourceforge import SourceforgePackage

from spack.package import *


class GhostscriptFonts(Package, SourceforgePackage):
    """Ghostscript Fonts"""

    homepage = "https://ghostscript.com/"
    sourceforge_mirror_path = (
        "gs-fonts/gs-fonts/8.11%20%28base%2035%2C%20GPL%29/ghostscript-fonts-std-8.11.tar.gz"
    )

    license("GPL-2.0-or-later")


    def install(self, spec, prefix):
        fdir = join_path(prefix.share, "font")
        mkdirp(fdir)
        files = glob.glob("*")
        for f in files:
            if not f.startswith("spack-build"):
                install(f, fdir)
