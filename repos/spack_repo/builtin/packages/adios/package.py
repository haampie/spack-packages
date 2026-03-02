# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Adios(AutotoolsPackage):
    """The Adaptable IO System (ADIOS) provides a simple,
    flexible way for scientists to describe the
    data in their code that may need to be written,
    read, or processed outside of the running simulation.
    """

    homepage = "https://www.olcf.ornl.gov/center-projects/adios/"
    url = "https://github.com/ornladios/ADIOS/archive/v1.12.0.tar.gz"
    git = "https://github.com/ornladios/ADIOS.git"



    variant("shared", default=True, description="Builds a shared version of the library")

    variant("fortran", default=False, description="Enable Fortran bindings support")


    # transforms
    variant("blosc", default=True, description="Enable Blosc transform support")
    # transports and serial file converters
    variant(
        "hdf5",
        default=False,
        description="Enable parallel HDF5 transport and serial bp2h5 " + "converter",
    )
    variant("netcdf", default=False, description="Enable netcdf support")

    variant(
        "staging",
        values=any_combination_of("flexpath", "dataspaces"),
        description="Enable dataspaces and/or flexpath staging transports",
    )

    # optional transformations
    # optional transports & file converters

    for p in ["+hdf5", "+netcdf", "staging=flexpath", "staging=dataspaces"]:
        conflicts(p, when="~mpi")

    build_directory = "spack-build"

    # ADIOS uses the absolute Python path, which is too long and results in
    # "bad interpreter" errors - but not applicable for 1.9.0
    # Fix ADIOS <=1.10.0 compile error on HDF5 1.10+
    #   https://github.com/ornladios/ADIOS/commit/3b21a8a41509
    #   https://github.com/spack/spack/issues/1683

    # ADIOS 1.13.1 is written for ZFP 0.5.0 interfaces
    #   https://github.com/ornladios/ADIOS/pull/204

    # Fix a bug in configure.ac that causes automake issues on RHEL 7.7

