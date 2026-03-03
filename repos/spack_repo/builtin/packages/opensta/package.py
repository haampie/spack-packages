# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Opensta(CMakePackage):
    """
    OpenSTA is a gate level static timing verifier. As a stand-alone executable
    it can be used to verify the timing of a design using standard file formats.

    * Verilog netlist
    * Liberty library
    * SDC timing constraints
    * SDF delay annotation
    * SPEF parasitics

    """

    homepage = "https://github.com/parallaxsw/OpenSTA"
    git = "https://github.com/parallaxsw/OpenSTA.git"

    maintainers("davekeeshan")

    license("GPL-3.0-only")

    version("master", branch="master")

    variant("zlib", default=True, description="build with zlib support")
    variant("cudd", default=True, description="build with cudd support")



    def cmake_args(self):
        args = []
        if self.spec.satisfies("+zlib"):
            args.append(f"-DZLIB_ROOT={self.spec['zlib'].prefix}")
        if self.spec.satisfies("+cudd"):
            args.append("-DUSE_CUDD=ON ")
            args.append(f"-DCUDD_DIR={self.spec['cudd'].prefix}")

        return args
