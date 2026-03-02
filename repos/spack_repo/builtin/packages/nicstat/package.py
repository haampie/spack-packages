# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.makefile import MakefilePackage
from spack_repo.builtin.build_systems.sourceforge import SourceforgePackage

from spack.package import *


class Nicstat(MakefilePackage, SourceforgePackage):
    """
    Nicstat is a Solaris and Linux command-line that prints out network
    statistics for all network interface cards (NICs), including packets,
    kilobytes per second, average packet sizes and more.
    """

    homepage = "https://github.com/scotte/nicstat"
    sourceforge_mirror_path = "nicstat/nicstat-1.95.tar.gz"




    def edit(self, spec, prefix):
        copy("Makefile.Linux", "makefile")
        filter_file(r"CMODEL =\s+-m32", "", "makefile")
        filter_file("sudo", "", "makefile", string=True)

    def install(self, spec, prefix):
        install_tree(".", prefix)
