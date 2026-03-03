# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import sys
from spack_repo.builtin.build_systems.cmake import CMakeBuilder, CMakePackage
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.rocm import ROCmPackage
from spack.package import *
class Viskores(CMakePackage, CudaPackage, ROCmPackage):
    """Viskores is a toolkit of scientific visualization algorithms for emerging
    processor architectures. Viskores supports the fine-grained concurrency for
    data analysis and visualization algorithms required to drive extreme scale
    computing by providing abstract models for data and execution that can be
    applied to a variety of algorithms across many different processor
    architectures."""
    homepage = "https://github.com/Viskores/viskores"
    url = "https://github.com/Viskores/Viskores/archive/refs/tags/v1.0.0.tar.gz"
    git = "https://github.com/Viskores/Viskores.git"
    tags = ["e4s"]
    test_requires_compiler = True
    variant("vtktypes", default=False, description="Build with VTK Types")
    variant("testlib", default=False, description="build test library")
    variant("fpic", default=False, description="build fpic support")
    variant("examples", default=False, description="Install builtin examples")
    # Device variants
    # CudaPackage provides cuda variant
    # ROCmPackage provides rocm variant
    # CUDA thrust is already include in the CUDA pkg
    depends_on("rocthrust", when="+kokkos+rocm ^cmake@3.24:")
    # It would be better if this could be expressed as a when clause to disable the rocm variant,
    # but that is not currently possible since when clauses are stacked, not overwritten.
    # Viskores uses the Kokkos SYCL backend.
    # If Kokkos provides multiple backends, the SYCL backend may or
    # may not be used for Viskores depending on the default selected by Kokkos
    depends_on("kokkos +sycl", when="+kokkos +sycl")
