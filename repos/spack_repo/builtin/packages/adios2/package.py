# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import sys
from spack_repo.builtin.build_systems.cmake import CMakeBuilder, CMakePackage
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.rocm import ROCmPackage
from spack.package import *
IS_WINDOWS = sys.platform == "win32"
class Adios2(CMakePackage, CudaPackage, ROCmPackage):
    """The Adaptable Input Output System version 2,
    developed in the Exascale Computing Program"""
    homepage = "https://adios2.readthedocs.io"
    url = "https://github.com/ornladios/ADIOS2/archive/v2.8.0.tar.gz"
    git = "https://github.com/ornladios/ADIOS2.git"
    # Compression libraries
    # Optional language bindings, C++11 and C always provided
    variant("kokkos", default=False, when="@2.9:", description="Enable Kokkos support")
    variant("sycl", default=False, when="@2.10:", description="Enable SYCL support")
    variant("python", default=False, description="Enable the Python bindings")
    variant("fortran", default=True, description="Enable the Fortran bindings")
    # Requires mature C++11 implementations
    # ifx does not support submodules in separate files
    # https://github.com/ornladios/ADIOS2/issues/4620
    with when("+kokkos"):
        depends_on("kokkos +rocm", when="+rocm")
