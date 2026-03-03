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
    depends_on("cxx", type="build")
    depends_on("apex", when="+apex")
    depends_on("python", type=("build", "test", "run"))
    depends_on("git", type="build")
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
    depends_on("mimalloc", when="malloc=mimalloc")
    depends_on("tbb", when="malloc=tbbmalloc")

    depends_on("mpi", when="networking=mpi")
    depends_on("mpi", when="+async_mpi")
    depends_on("lci", when="networking=lci")

    depends_on("cuda", when="+async_cuda")

    depends_on("gperftools", when="instrumentation=google_perftools")
    depends_on("papi", when="instrumentation=papi")
    depends_on("valgrind", when="instrumentation=valgrind")

    # Only ROCm or CUDA maybe be enabled at once
    conflicts("+rocm", when="+cuda")

    # Restrictions for 1.9.X
    with when("@1.9:"):
        conflicts("%gcc@:8")
        conflicts("%clang@:9")

    # Restrictions for 1.8.X
    with when("@1.8:"):
        conflicts("cxxstd=14")
        conflicts("%gcc@:7")
        conflicts("%clang@:8")
        depends_on("cuda@11:", when="+cuda")

    # Restrictions for 1.7.X
    with when("@1.7:"):
        depends_on("cmake@3.18.0:", type="build")
        depends_on("boost@1.71.0:")
        depends_on("asio@1.12.0:")
        conflicts("%gcc@:6")
        conflicts("%clang@:6")

    # Restrictions for 1.6.X

    # Restrictions for 1.5.x
    depends_on("apex@2.3:", when="@1.5")

    # Restrictions for 1.2.X
    with when("@:1.2.1"):
        depends_on("cmake@3.9.0:", type="build")
        depends_on("boost@1.62.0:")
        depends_on("hwloc@1.11:")

    # Restrictions before 1.2
    with when("@:1.1.0"):
        depends_on("boost@1.55.0:")
        depends_on("hwloc@1.6:")

    # Patches and one-off conflicts

    # Asio 1.34.0 removed io_context::work, used by HPX:
    # https://github.com/chriskohlhoff/asio/commit/a70f2df321ff40c1809773c2c09986745abf8d20.

    # Certain Asio headers don't compile with nvcc from 1.17.0 onwards with
    # C++17. Starting with CUDA 11.3 they compile again.

    # Starting from ROCm 5.0.0 hipcc miscompiles asio 1.17.0 and newer

    # Boost and HIP don't work together in certain versions:
    # https://github.com/boostorg/config/issues/392. Boost 1.78.0 and HPX 1.8.0
    # both include a fix.

    # libstdc++ has a broken valarray in some versions that clang/hipcc refuses
    # to compile:
    # https://github.com/spack/spack/issues/38104
    # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=103022

    # boost 1.73.0 build problem with HPX 1.4.0 and 1.4.1
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


    def url_for_version(self, version):
        if version >= Version("1.9.0"):
            return "https://github.com/STEllAR-GROUP/hpx/archive/v{}.tar.gz".format(version)
        return "https://github.com/STEllAR-GROUP/hpx/archive/{}.tar.gz".format(version)

    def instrumentation_args(self):
        args = []
        for value in self.instrumentation_values:
            condition = "instrumentation={0}".format(value)
            args.append(self.define("HPX_WITH_{0}".format(value.upper()), condition in self.spec))
        return args

    def cmake_args(self):
        spec, args = self.spec, []

        format_max_cpu_count = lambda max_cpu_count: (
            "" if max_cpu_count == "auto" else max_cpu_count
        )
        args += [
            self.define("HPX_WITH_CXX{0}".format(spec.variants["cxxstd"].value), True),
            self.define_from_variant("HPX_WITH_MALLOC", "malloc"),
            self.define_from_variant("HPX_WITH_CUDA", "cuda"),
            self.define_from_variant("HPX_WITH_HIP", "rocm"),
            self.define_from_variant("HPX_WITH_TOOLS", "tools"),
            self.define_from_variant("HPX_WITH_EXAMPLES", "examples"),
            self.define_from_variant("HPX_WITH_ASYNC_MPI", "async_mpi"),
            self.define_from_variant("HPX_WITH_ASYNC_CUDA", "async_cuda"),
            self.define_from_variant("HPX_WITH_APEX", "apex"),
            self.define("HPX_WITH_TESTS", self.run_tests),
            self.define("HPX_WITH_NETWORKING", "networking=none" not in spec),
            self.define("HPX_WITH_PARCELPORT_TCP", spec.satisfies("networking=tcp")),
            self.define("HPX_WITH_PARCELPORT_MPI", spec.satisfies("networking=mpi")),
            self.define("HPX_WITH_PARCELPORT_LCI", spec.satisfies("networking=lci")),
            self.define(
                "HPX_WITH_MAX_CPU_COUNT",
                format_max_cpu_count(spec.variants["max_cpu_count"].value),
            ),
            self.define_from_variant("HPX_WITH_GENERIC_CONTEXT_COROUTINES", "generic_coroutines"),
            self.define("BOOST_ROOT", spec["boost"].prefix),
            self.define("HWLOC_ROOT", spec["hwloc"].prefix),
            self.define("HPX_WITH_BOOST_ALL_DYNAMIC_LINK", True),
            self.define("BUILD_SHARED_LIBS", True),
            self.define("HPX_DATASTRUCTURES_WITH_ADAPT_STD_TUPLE", False),
            self.define("HPX_WITH_PKGCONFIG", False),
        ]

        # Enable unity builds when available
        if spec.satisfies("@1.7:"):
            args += [self.define("HPX_WITH_UNITY_BUILD", True)]

        # HIP support requires compiling with hipcc
        if self.spec.satisfies("+rocm"):
            args += [self.define("CMAKE_CXX_COMPILER", self.spec["hip"].hipcc)]
            if self.spec.satisfies("^cmake@3.21.0:3.21.2"):
                args += [self.define("__skip_rocmclang", True)]

        # Instrumentation
        args += self.instrumentation_args()

        if spec.satisfies("instrumentation=thread_debug"):
            args += [
                self.define("HPX_WITH_THREAD_DEBUG_INFO", True),
                self.define("HPX_WITH_LOGGING", True),
            ]

        return args
