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
    variant("shared", default=True, description="build shared libs")
    variant("doubleprecision", default=True, description="enable double precision")
    variant("logging", default=True, description="build logging support")
    variant("mpi", default=True, description="build mpi support")
    variant("rendering", default=True, description="build rendering support")
    variant("64bitids", default=False, description="enable 64 bits ids")
    variant("vtktypes", default=False, description="Build with VTK Types")
    variant("testlib", default=False, description="build test library")
    variant("fpic", default=False, description="build fpic support")
    variant("examples", default=False, description="Install builtin examples")
    # Device variants
    # CudaPackage provides cuda variant
    # ROCmPackage provides rocm variant
    variant("kokkos", default=False, description="build using Kokkos backend")
    variant(
        "cuda_native", default=True, description="build using native cuda backend", when="+cuda"
    )
    variant("openmp", default=(sys.platform != "darwin"), description="build openmp support")
    variant("tbb", default=(sys.platform == "darwin"), description="build TBB support")
    variant("sycl", default=False, description="Build with SYCL backend")
    depends_on("tbb", when="+tbb")
    # Viskores uses the default Kokkos backend
    # Viskores native CUDA and Kokkos CUDA backends are not compatible
    depends_on("kokkos ~cuda", when="+kokkos +cuda +cuda_native")
    depends_on("kokkos +cuda", when="+kokkos +cuda ~cuda_native")
    for cuda_arch in CudaPackage.cuda_arch_values:
        depends_on(
            "kokkos cuda_arch=%s" % cuda_arch,
            when="+kokkos +cuda ~cuda_native cuda_arch=%s" % cuda_arch,
        )
    # Viskores uses the Kokkos HIP backend.
    # If Kokkos provides multiple backends, the HIP backend may or
    # may not be used for Viskores depending on the default selected by Kokkos
    depends_on("kokkos +rocm", when="+kokkos +rocm")
    # Propagate AMD GPU target to kokkos for +rocm
    for amdgpu_value in ROCmPackage.amdgpu_targets:
        depends_on(
            "kokkos amdgpu_target=%s" % amdgpu_value,
            when="+kokkos +rocm amdgpu_target=%s" % amdgpu_value,
        )
    # CUDA thrust is already include in the CUDA pkg
    # It would be better if this could be expressed as a when clause to disable the rocm variant,
    # but that is not currently possible since when clauses are stacked, not overwritten.
    # Viskores uses the Kokkos SYCL backend.
    # If Kokkos provides multiple backends, the SYCL backend may or
    # may not be used for Viskores depending on the default selected by Kokkos
