# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.rocm import ROCmPackage

from spack.package import *


class HpxKokkos(CMakePackage, CudaPackage, ROCmPackage):
    """HPXKokkos is an interoperability library for HPX and Kokkos"""

    homepage = "https://github.com/STEllAR-GROUP/hpx-kokkos"
    url = "https://github.com/STEllAR-GROUP/hpx-kokkos/archive/0.0.0.tar.gz"
    git = "https://github.com/STEllAR-GROUP/hpx-kokkos.git"



    cxxstds = ("14", "17", "20")
    variant(
        "cxxstd",
        default="14",
        values=cxxstds,
        description="Use the specified C++ standard when building.",
    )

    future_types_map = {"polling": "event", "callback": "callback"}
    variant(
        "future_type",
        default="polling",
        values=tuple(future_types_map.keys()),
        description="Integration type for GPU futures",
    )

    depends_on("cxx", type="build")

    depends_on("cmake@3.19:", type="build")

    depends_on("hpx")
    depends_on("kokkos +hpx +hpx_async_dispatch")

    depends_on("hpx@1.8:", when="@0.3:")
    depends_on("kokkos@3.6:", when="@0.3:")
    # Incompatibilities caused by https://github.com/STEllAR-GROUP/hpx/pull/6565
    # and https://github.com/kokkos/kokkos/pull/7156 fixed by
    # https://github.com/STEllAR-GROUP/hpx-kokkos/pull/25
    conflicts("^hpx@1.11:", when="@:0.4.0")
    conflicts("^kokkos@4.4:", when="@:0.4.0")

    depends_on("hpx@1.7", when="@0.2")
    depends_on("kokkos@3.6:", when="@0.2")

    for cxxstd in cxxstds:
        depends_on("hpx cxxstd={0}".format(cxxstd), when="cxxstd={0}".format(cxxstd))
        depends_on("kokkos cxxstd={0}".format(cxxstd), when="cxxstd={0}".format(cxxstd))

    # HPXKokkos explicitly supports CUDA and ROCm. Other GPU backends can be
    # used but without support in HPXKokkos. Other CPU backends, except Serial,
    # can't be used together with the HPX backend.
    depends_on("hpx +cuda", when="+cuda")
    depends_on("kokkos +cuda +cuda_lambda +cuda_constexpr", when="+cuda")

    depends_on("hpx +rocm", when="+rocm")
    depends_on("kokkos +rocm", when="+rocm")

    def cmake_args(self):
        spec, args = self.spec, []

        args += [
            self.define(
                "HPX_KOKKOS_CUDA_FUTURE_TYPE",
                self.future_types_map[spec.variants["future_type"].value],
            ),
            self.define("HPX_KOKKOS_ENABLE_TESTS", self.run_tests),
            self.define("HPX_KOKKOS_ENABLE_BENCHMARKS", self.run_tests),
        ]

        if self.spec.satisfies("+rocm"):
            args += [self.define("CMAKE_CXX_COMPILER", self.spec["hip"].hipcc)]

        return args

    build_directory = "spack-build"

    def check(self):
        if self.run_tests:
            with working_dir(self.build_directory):
                cmake("--build", ".", "--target", "tests")
                cmake("--build", ".", "--target", "benchmarks")
                ctest("--output-on-failure")
