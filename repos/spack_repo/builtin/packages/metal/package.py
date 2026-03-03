# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Metal(CMakePackage):
    """METAL is a tool for the meta-analysis of genome-wide association studies"""

    homepage = "https://genome.sph.umich.edu/wiki/METAL"
    url = "https://github.com/statgen/METAL/archive/refs/tags/2020-05-05.tar.gz"


    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.1:", type="build")
    depends_on("zlib-ng")

    @run_after("install")
    def mv_binary(self):
        with working_dir(self.build_directory):
            install_tree("bin", self.prefix.bin)
