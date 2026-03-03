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


    version("develop", branch="master")
    version("1.13.1", sha256="b1c6949918f5e69f701cabfe5987c0b286793f1057d4690f04747852544e157b")
    version("1.13.0", sha256="7b5ee8ff7a5f7215f157c484b20adb277ec0250f87510513edcc25d2c4739f50")
    version("1.12.0", sha256="22bc22c157322abec2d1a0817a259efd9057f88c2113e67d918a9a5ebcb3d88d")
    version("1.11.1", sha256="9f5c10b9471a721ba57d1cf6e5a55a7ad139a6c12da87b4dc128539e9eef370e")
    version("1.11.0", sha256="e89d14ccbe7181777225e0ba6c272c0941539b8ccd440e72ed5a9457441dae83")
    version("1.10.0", sha256="6713069259ee7bfd4d03f47640bf841874e9114bab24e7b0c58e310c42a0ec48")
    version("1.9.0", sha256="23b2bb70540d51ab0855af0b205ca484fd1bd963c39580c29e3133f9e6fffd46")

    variant("shared", default=True, description="Builds a shared version of the library")



    # transforms
    variant("lz4", default=True, description="Enable LZ4 transform support")
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

