# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class Rdptools(MakefilePackage):
    """Collection of commonly used RDP Tools for easy building."""

    homepage = "https://github.com/rdpstaff/RDPTools"
    url = "https://github.com/rdpstaff/RDPTools/archive/2.0.2.tar.gz"


    # https://github.com/bioconda/bioconda-recipes/blob/master/recipes/rdptools/meta.yaml
    depends_on("java")
    depends_on("ant")
    depends_on("python")

    def install(self, spec, prefix):
        install_tree(".", prefix)
