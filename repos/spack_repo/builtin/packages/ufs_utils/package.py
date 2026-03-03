# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class UfsUtils(CMakePackage):
    """The UFS Utilities package contains programs set up the model grid and
    create coldstart initial conditions.

    This is related to NOAA's NCEPLIBS project."""

    homepage = "https://noaa-emcufs-utils.readthedocs.io/en/latest/"
    url = "https://github.com/NOAA-EMC/UFS_UTILS/archive/refs/tags/ufs_utils_1_7_0.tar.gz"
    git = "https://github.com/ufs-community/UFS_UTILS"



    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("mpi")
    depends_on("cmake@3.23:")
    depends_on("bacio")
    depends_on("esmf")
    depends_on("g2")
    depends_on("hdf5")
    depends_on("ip")
    depends_on("jasper")
    depends_on("libpng")
    depends_on("nemsio")
    depends_on("netcdf-c")
    depends_on("netcdf-fortran")
    depends_on("sfcio")
    depends_on("sigio")
    depends_on("sp")
    depends_on("w3emc")
    depends_on("zlib-api")

    def cmake_args(self):
        return [
            "-DMPI_C_COMPILER=%s" % self.spec["mpi"].mpicc,
            "-DMPI_Fortran_COMPILER=%s" % self.spec["mpi"].mpifc,
        ]

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        env.set("ESMFMKFILE", join_path(self.spec["esmf"].prefix.lib, "esmf.mk"))
