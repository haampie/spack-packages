# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Filo(CMakePackage):
    """File flush and fetch, with MPI"""

    homepage = "https://github.com/ecp-veloc/filo"
    git = "https://github.com/ecp-veloc/filo.git"

    tags = ["ecp"]

    version("main", branch="main")



    def cmake_args(self):
        args = []
        args.append("-DMPI_C_COMPILER=%s" % self.spec["mpi"].mpicc)
        args.append("-DWITH_AXL_PREFIX=%s" % self.spec["axl"].prefix)
        args.append("-DWITH_KVTREE_PREFIX=%s" % self.spec["kvtree"].prefix)
        args.append("-DWITH_SPATH_PREFIX=%s" % self.spec["spath"].prefix)
        return args
