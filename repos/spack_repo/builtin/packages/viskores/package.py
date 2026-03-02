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
    variant(
        "cuda_native", default=True, description="build using native cuda backend", when="+cuda"
    )
    variant("openmp", default=(sys.platform != "darwin"), description="build openmp support")
    variant("tbb", default=(sys.platform == "darwin"), description="build TBB support")
    variant("sycl", default=False, description="Build with SYCL backend")
    depends_on("tbb", when="+tbb")
    # Viskores uses the default Kokkos backend
