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


    generator("ninja")

    cxxstds = ("11", "14", "17", "20", "23")
    variant(
        "cxxstd",
        default="17",
        values=cxxstds,
        description="Use the specified C++ standard when building.",
    )

    variant(
        "malloc",
        default="tcmalloc",
        description="Define which allocator will be linked in",
        values=("system", "jemalloc", "mimalloc", "tbbmalloc", "tcmalloc"),
    )

    variant(
        "max_cpu_count",
        default="auto",
        description="Max number of OS-threads for HPX applications",
        values=lambda x: isinstance(x, str) and (x.isdigit() or x == "auto"),
    )

    instrumentation_values = ("google_perftools", "papi", "valgrind", "thread_debug")
    variant(
        "instrumentation",
        values=any_combination_of(*instrumentation_values),
        description="Add support for various kind of instrumentation",
    )

    variant(
        "networking",
        values=any_combination_of("tcp", "mpi", "lci").with_default("tcp"),
        description="Support for networking through parcelports",
    )

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
    variant("async_cuda", default=False, description="Enable CUDA Futures.")
    variant("apex", default=False, description="Enable APEX support")

    # Build dependencies
    depends_on("cmake", type="build")

    # Other dependecies
    depends_on("hwloc")
    depends_on(Boost.with_default_variants)
    depends_on("boost +context", when="+generic_coroutines")
    for cxxstd in cxxstds:
        depends_on(f"boost cxxstd={cxxstd}", when=f"cxxstd={cxxstd}")
        depends_on(f"asio cxxstd={cxxstd}", when=f"@1.7: cxxstd={cxxstd}")

    depends_on("gperftools", when="malloc=tcmalloc")
    depends_on("jemalloc", when="malloc=jemalloc")




    # Only ROCm or CUDA maybe be enabled at once
    conflicts("+rocm", when="+cuda")

    # Restrictions for 1.9.X
    with when("@1.9:"):
        conflicts("%gcc@:8")
        conflicts("%clang@:9")
    # Restrictions for 1.8.X
    with when("@1.8:"):
        conflicts("%gcc@:7")
        conflicts("%clang@:8")

        conflicts("%gcc@:6")
        conflicts("%clang@:6")

    # Restrictions for 1.5.x

    # Restrictions for 1.2.X
    with when("@:1.2.1"):
        depends_on("hwloc@1.11:")

    with when("@:1.1.0"):
        depends_on("boost@1.55.0:")
        depends_on("hwloc@1.6:")
    # Asio 1.34.0 removed io_context::work, used by HPX:
    # https://github.com/chriskohlhoff/asio/commit/a70f2df321ff40c1809773c2c09986745abf8d20.

    # Certain Asio headers don't compile with nvcc from 1.17.0 onwards with
    # C++17. Starting with CUDA 11.3 they compile again.


    # Boost and HIP don't work together in certain versions:
    # https://github.com/boostorg/config/issues/392. Boost 1.78.0 and HPX 1.8.0
    # to compile:
    # https://github.com/spack/spack/issues/38104
    # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=103022
    # https://github.com/STEllAR-GROUP/hpx/issues/4728#issuecomment-640685308
    depends_on("boost@:1.72.0", when="@:1.4")

    # COROUTINES
    # ~generic_coroutines conflict is not fully implemented
    # for additional information see:
    # https://github.com/spack/spack/pull/17654
    # https://github.com/STEllAR-GROUP/hpx/issues/4829
    depends_on("boost+context", when="+generic_coroutines")

    _msg_generic_coroutines_platform = "This platform requires +generic_coroutines"

    _msg_generic_coroutines_target = "This target requires +generic_coroutines"


