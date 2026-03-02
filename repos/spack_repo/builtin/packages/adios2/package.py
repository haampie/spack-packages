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
    test_requires_compiler = True


    tags = ["e4s"]



    # There's not really any consistency about how static and shared libs are
    # implemented across spack.  What we're trying to support is specifically three
    # library build types:
    #   shared (which is implicitly w/ pic)
    #     Implemented by +shared +pic
    #   static w/o pic
    #     Implemented by ~shared ~pic
    #   static w/ pic
    #     Implemented by ~shared +pic
    # shared w/o pic is not a valid configuration because shared libraries are Position
    # Independent # Code by design.  We're not inherently tied to this approach and can
    # change how we're supporting differnt library types in the package at anytime if
    # spack decides on a standardized way of doing it across packages
    variant("shared", default=True, when="+pic", description="Build shared libraries")

    # Features
    variant("mpi", default=True, description="Enable MPI")

    # Compression libraries
    variant(
        "libpressio", default=False, when="@2.8:", description="Enable LibPressio for compression"
    )
    variant("blosc", default=True, when="@2.4:2.8", description="Enable Blosc compression")
    variant("blosc2", default=True, when="@2.9:", description="Enable Blosc2 compression")
    variant("bzip2", default=True, description="Enable BZip2 compression")
    variant("zfp", default=True, description="Enable ZFP compression")
    variant("png", default=True, description="Enable PNG compression")
    variant("sz", default=True, description="Enable SZ2 compression")
    variant("sz3", default=True, when="@2.12:", description="Enable SZ3 compression")
    variant("mgard", default=not IS_WINDOWS, when="@2.8:", description="Enable MGARD compression")

    # Rransport engines
    variant("sst", default=True, description="Enable the SST staging engine")
    variant("hdf5", default=False, description="Enable the HDF5 engine")
    variant(
        "aws",
        default=False,
        when="@2.9:",
        description="Enable support for S3 compatible storage using AWS SDK's S3 module",
    )
    variant(
        "libcatalyst",
        default=not IS_WINDOWS,
        when="@2.9:",
        description="Enable support for in situ visualization plugin using ParaView Catalyst",
    )

    variant("xrootd", default=True, description="Enable the XRootD")

    # Optional language bindings, C++11 and C always provided
    variant("kokkos", default=False, when="@2.9:", description="Enable Kokkos support")
    variant("sycl", default=False, when="@2.10:", description="Enable SYCL support")
    variant("python", default=False, description="Enable the Python bindings")
    variant("fortran", default=True, description="Enable the Fortran bindings")

    # Requires mature C++11 implementations

    # ifx does not support submodules in separate files
    # https://github.com/ornladios/ADIOS2/issues/4620


    # Standalone CUDA support
    # Kokkos support
    with when("+kokkos"):
        depends_on("kokkos +rocm", when="+rocm")
        depends_on("kokkos +sycl", when="+sycl")

    # Propagate CUDA target to kokkos for +cuda
    for cuda_arch in CudaPackage.cuda_arch_values:
        depends_on(
            "kokkos cuda_arch=%s" % cuda_arch, when="+kokkos +cuda cuda_arch=%s" % cuda_arch
        )

    # Propagate AMD GPU target to kokkos for +rocm
    for amdgpu_value in ROCmPackage.amdgpu_targets:
        depends_on(
            "kokkos amdgpu_target=%s" % amdgpu_value,
            when="+kokkos +rocm amdgpu_target=%s" % amdgpu_value,
        )




    for _platform in ["linux", "darwin"]:
        variant(
            "pic",
            default=False,
            description="Build pic-enabled static libraries",
            when=f"platform={_platform}",
        )
        # libffi and libfabric and not currently supported on Windows
        # see Paraview's superbuild handling of libfabric at
        # https://gitlab.kitware.com/paraview/paraview-superbuild/-/blob/master/projects/adios2.cmake#L3
        # depends_on('bison', when='+sst')     # optional in FFS, broken package
        # depends_on('flex', when='+sst')      # optional in FFS, depends on BISON



    depends_on("mgard@compat-2023-01-10:", when="@2.9: +mgard")
    # cmake build race condition

    # add missing include <cstdint>

    # Add missing include <memory>
    # https://github.com/ornladios/adios2/pull/2710

    # https://github.com/ornladios/ADIOS2/pull/3893

    # ROCM: enable support for rocm >= 6

    # Fix issue with GCC 7
    # https://github.com/ornladios/ADIOS2/pull/4591

    # https://github.com/ornladios/ADIOS2/pull/4729

