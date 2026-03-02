# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class Fraggenescan(MakefilePackage):
    """FragGeneScan is an application for finding (fragmented) genes in short
    reads. It can also be applied to predict prokaryotic genes in
    incomplete assemblies or complete genomes."""

    homepage = "https://sourceforge.net/projects/fraggenescan/"
    url = "https://downloads.sourceforge.net/project/fraggenescan/FragGeneScan1.31.tar.gz"


    depends_on("c", type="build")  # generated

    def edit(self, spec, prefix):
        filter_file("gcc", spack_cc, "Makefile", string=True)

    def build(self, spec, prefic):
        make("clean")
        make("fgs")

    def install(self, spec, prefix):
        install_tree(".", prefix.bin)
