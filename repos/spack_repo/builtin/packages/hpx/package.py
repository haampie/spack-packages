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
    # Other dependecies
    depends_on("boost +context", when="+generic_coroutines")
