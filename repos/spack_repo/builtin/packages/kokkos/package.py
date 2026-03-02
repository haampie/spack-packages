# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.rocm import ROCmPackage
from spack.package import *
class Kokkos(CMakePackage, CudaPackage, ROCmPackage):
    """Kokkos implements a programming model in C++ for writing performance
    portable applications targeting all major HPC platforms."""
    homepage = "https://github.com/kokkos/kokkos"
    git = "https://github.com/kokkos/kokkos.git"
    url = "https://github.com/kokkos/kokkos/releases/download/4.4.01/kokkos-4.4.01.tar.gz"
    tags = ["e4s"]
    test_requires_compiler = True
    options_variants = {
        "debug_dualview_modify_check": [False, "@:4", "Debug check on dual views"],
        "86": "ampere86",
        "87": "ampere87",
        "89": "ada89",
        "90": "hopper90",
        "100": "blackwell100",
        "120": "blackwell120",
    }
    variant("apu", default=False, description="Enable APU support", when="@4.5: +rocm")
