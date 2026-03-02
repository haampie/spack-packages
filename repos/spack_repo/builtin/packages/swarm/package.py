# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class Swarm(MakefilePackage):
    """A robust and fast clustering method for amplicon-based studies."""

    homepage = "https://github.com/torognes/swarm"
    url = "https://github.com/torognes/swarm/archive/v2.1.13.tar.gz"

    license("AGPL-3.0-only")




    build_directory = "src"

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
        install_tree("scripts", prefix.scripts)
        install_tree("man", prefix.share.man)
