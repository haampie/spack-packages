# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class Savanna(MakefilePackage):
    """CODARcode Savanna runtime framework for high performance,
    workflow management using Swift/T and ADIOS.
    """

    homepage = "https://github.com/CODARcode/savanna"
    git = "https://github.com/CODARcode/savanna.git"

    version("develop", branch="master", submodules=True)
    version("0.5", tag="0.5", submodules=True)

    variant("tau", default=False, description="Enable TAU profiling support")


    def install(self, spec, prefix):
        install_tree(".", prefix)
