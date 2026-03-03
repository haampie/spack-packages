# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class Filtlong(MakefilePackage):
    """Filtlong is a tool for filtering long reads by quality. It can
    take a set of long reads and produce a smaller, better subset."""

    homepage = "https://github.com/rrwick/Filtlong"
    url = "https://github.com/rrwick/Filtlong/archive/v0.2.0.tar.gz"




    # %gcc@13: requires std libraries be manually added - add an include for `cstdint`
    patch("gcc13.patch", level=0, when="%gcc@13:")

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install_tree("bin", prefix.bin)

        mkdir(prefix.test)
        install_tree("test", prefix.test)
