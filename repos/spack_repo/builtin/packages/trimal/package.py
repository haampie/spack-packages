# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class Trimal(MakefilePackage):
    """A tool for automated alignment trimming in large-scale
    phylogenetic analyses"""

    homepage = "https://github.com/scapella/trimal"
    url = "https://github.com/scapella/trimal/archive/v1.4.1.tar.gz"

    license("GPL-3.0-or-later")



    build_directory = "source"

    def install(self, sinstall_treepec, prefix):
        mkdirp(prefix.bin)
        binaries = ["trimal", "readal", "statal"]
        with working_dir(self.build_directory):
            for b in binaries:
                install(b, prefix.bin)
