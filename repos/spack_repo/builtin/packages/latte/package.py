# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Latte(CMakePackage):
    """Open source density functional tight binding molecular dynamics."""

    homepage = "https://github.com/lanl/latte"
    url = "https://github.com/lanl/latte/tarball/v1.2.1"
    git = "https://github.com/lanl/latte.git"


    tags = ["ecp", "ecp-apps"]



    variant("interface", default=False, description="Build with interfacing to use with sedacs")
    variant("mpi", default=True, description="Build with mpi")
    variant("progress", default=False, description="Use progress for fast solvers")
    variant("shared", default=True, description="Build shared libs")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated
    depends_on("cmake@3.1:", type="build")
    depends_on("blas")
    depends_on("lapack")
    depends_on("mpi", when="+mpi")
    depends_on("qmd-progress", when="+progress")

    root_cmakelists_dir = "cmake"

    def cmake_args(self):
        options = []
        if self.spec.satisfies("+shared"):
            options.append("-DBUILD_SHARED_LIBS=ON")
        else:
            options.append("-DBUILD_SHARED_LIBS=OFF")
        if self.spec.satisfies("+mpi"):
            options.append("-DDO_MPI=ON")
            options.append("-DCMAKE_C_COMPILER=%s" % self.spec["mpi"].mpicc)
            options.append("-DCMAKE_CXX_COMPILER=%s" % self.spec["mpi"].mpicxx)
            options.append("-DCMAKE_Fortran_COMPILER=%s" % self.spec["mpi"].mpifc)
        if self.spec.satisfies("+progress"):
            options.append("-DPROGRESS=ON")

        if self.spec.satisfies("+interface"):
            options.append("-DMAKELIB=ON")

        # specify blas/lapack libs
        options.append("-DBLAS_LIBRARIES=%s" % self.spec["blas"].libs)
        options.append("-DLAPACK_LIBRARIES=%s" % self.spec["lapack"].libs)

        # flag needed to remove gfortran max line length constraint
        options.append("-DCMAKE_Fortran_FLAGS=-ffree-line-length-none")

        return options
