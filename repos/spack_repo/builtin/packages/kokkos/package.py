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
    with when("@5:"):
        conflicts("%msvc@:19.2")
    conflicts("^cmake@3.28", when="@:4.2.01 +cuda")
    devices_variants = {
        "cuda": [False, "Whether to build CUDA backend"],
        "openmp": [False, "Whether to build OpenMP backend"],
        "threads": [False, "Whether to build the C++ threads backend"],
        "serial": [False, "Whether to build serial backend"],
        "rocm": [False, "Whether to build HIP backend"],
        "debug": [False, None, "Activate extra debug features - may increase compiletimes"],
        "debug_bounds_check": [False, None, "Use bounds checking - will increase runtime"],
        "debug_dualview_modify_check": [False, "@:4", "Debug check on dual views"],
        "deprecated_code": [False, "@:4", "Whether to enable deprecated code"],
        "examples": [False, "@:4", "Whether to build examples"],
        "hpx_async_dispatch": [False, "@:4", "Whether HPX supports asynchronous dispath"],
        "icelake": "ICL",
        "skylake_avx512": "SKX",
        "sapphirerapids": "SPR",
    }
    spack_cuda_arch_map = {
        "30": "kepler30",
        "32": "kepler32",
        "35": "kepler35",
        "37": "kepler37",
        "50": "maxwell50",
        "52": "maxwell52",
        "53": "maxwell53",
        "60": "pascal60",
        "61": "pascal61",
        "70": "volta70",
        "72": "volta72",
        "75": "turing75",
        "80": "ampere80",
        "86": "ampere86",
        "87": "ampere87",
        "89": "ada89",
        "90": "hopper90",
        "100": "blackwell100",
        "120": "blackwell120",
    }
    cuda_arches = spack_cuda_arch_map.values()
    conflicts("+cuda", when="cuda_arch=none")
    # Kokkos support only one cuda_arch at a time
    conflicts("+openmptarget", when="cxxstd=14", msg="OpenMPTarget requires C++17 or higher")
    # HPX should use the same C++ standard
    for cxxstd in ["14", "17", "20", "23"]:
        depends_on(f"hpx cxxstd={cxxstd}", when=f"+hpx cxxstd={cxxstd}")
    # HPX version constraints
    # Patches
    # spack compiler wrappers
    # sanity check
    sanity_check_is_dir = ["bin", "include"]
    test_script_relative_path = join_path("scripts", "spack_test")
