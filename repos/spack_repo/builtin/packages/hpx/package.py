# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import sys
from spack_repo.builtin.build_systems.cmake import CMakePackage, generator
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.rocm import ROCmPackage
from spack_repo.builtin.packages.boost.package import Boost
from spack.package import *
class Hpx(CMakePackage, CudaPackage, ROCmPackage):
    """C++ runtime system for parallel and distributed applications."""
    homepage = "https://hpx.stellar-group.org/"
    url = "https://github.com/STEllAR-GROUP/hpx/archive/v0.0.0.tar.gz"
    git = "https://github.com/STEllAR-GROUP/hpx.git"
    tags = ["e4s"]
    cxxstds = ("11", "14", "17", "20", "23")
    variant(
        "cxxstd",
        default="17",
        values=cxxstds,
        description="Use the specified C++ standard when building.",
    )
    instrumentation_values = ("google_perftools", "papi", "valgrind", "thread_debug")
    default_generic_coroutines = True
    if sys.platform.startswith("linux") or sys.platform == "win32":
        default_generic_coroutines = False
    variant(
        "generic_coroutines",
        default=default_generic_coroutines,
        description="Use Boost.Context as the underlying coroutines"
        " context switch implementation.",
    )
    variant("tools", default=False, description="Build HPX tools")
    variant("examples", default=False, description="Build examples")
    variant("async_mpi", default=False, description="Enable MPI Futures.")
    # Build dependencies
    # Other dependecies
    depends_on("boost +context", when="+generic_coroutines")
    for cxxstd in cxxstds:
        depends_on(f"boost cxxstd={cxxstd}", when=f"cxxstd={cxxstd}")
    # Only ROCm or CUDA maybe be enabled at once
    # Restrictions for 1.9.X
    with when("@1.9:"):
        conflicts("%gcc@:8")
        conflicts("%clang@:9")
    # Restrictions for 1.8.X
    with when("@1.8:"):
        conflicts("cxxstd=14")
        conflicts("%gcc@:7")
    # Restrictions for 1.7.X
    _msg_generic_coroutines_target = "This target requires +generic_coroutines"
