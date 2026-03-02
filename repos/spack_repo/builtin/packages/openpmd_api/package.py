# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class OpenpmdApi(CMakePackage):
    """C++ & Python API for Scientific I/O"""

    homepage = "https://www.openPMD.org"
    url = "https://github.com/openPMD/openPMD-api/archive/0.17.0.tar.gz"
    git = "https://github.com/openPMD/openPMD-api.git"


    tags = ["e4s"]


    # C++17 up until here
    # C++14 up until here
    version("0.14.2", sha256="25c6b4bcd0ae1ba668b633b8514e66c402da54901c26861fc754fca55717c836")
    # C++11 up until here

    variant("mpi", default=True, description="Enable parallel I/O")
    variant("hdf5", default=True, description="Enable HDF5 support")
    variant("adios1", default=False, description="Enable ADIOS1 support", when="@:0.15")
    variant("adios2", default=True, description="Enable ADIOS2 support")
    variant("python", default=False, description="Enable Python bindings")

    depends_on("c", type="build")
    depends_on("cmake@3.15.0:", type="build")
    depends_on("toml11@3.7.1:", when="@0.16:")
    depends_on("toml11@4.2.0: cxx_std=17", when="@0.16.1:")
    with when("+hdf5"):
        depends_on("hdf5@1.8.13:")
        depends_on("hdf5@1.8.13: ~mpi", when="~mpi")
        depends_on("hdf5@1.8.13: +mpi", when="+mpi")
        depends_on("adios@1.13.1: ~sz")
    with when("+python"):
        depends_on("py-numpy@1.15.1:", type=("test", "run"))
        depends_on("py-mpi4py@2.1.0:", when="+mpi", type=("test", "run"))
        with default_args(type=("link", "test", "run")):
            depends_on("python@3.7:")


    # https://github.com/openPMD/openPMD-api/pull/1012
    # CMake: Fix Python Install Directory

    # macOS AppleClang12 Fixes

    # forgot to bump version.hpp in 0.15.1

    # fix superbuild control in 0.16.0

    extends("python", when="+python")

