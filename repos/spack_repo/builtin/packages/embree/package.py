# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Embree(CMakePackage):
    """Intel Embree High Performance Ray Tracing Kernels"""

    homepage = "https://embree.org"
    url = "https://github.com/embree/embree/archive/v3.7.0.tar.gz"


    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("ispc", default=True, description="Enable ISPC support")
    depends_on("ispc", when="+ispc", type="build")

    depends_on("tbb")

    # official aarch64 support on macOS starting with 3.13.0, on Linux since 4.0.0
    # upstream patch for Linux/aarch64 applies cleanly to 3.13.5, and 3.13.3 works by chance
    conflicts("@:3.12", when="target=aarch64:")
    conflicts("@:3.13.2", when="target=aarch64: platform=linux")
    conflicts("@3.13.4", when="target=aarch64: platform=linux")
    patch(
        "https://github.com/embree/embree/commit/82ca6b5ccb7abe0403a658a0e079926478f04cb1.patch?full_index=1",
        sha256="3af5a65e8875549b4c930d4b0f2840660beba4a7f295d8c89068250a1df376f2",
        when="@3.13.5",
    )

    def cmake_args(self):
        spec = self.spec

        args = [
            self.define("BUILD_TESTING", self.run_tests),
            self.define("EMBREE_TUTORIALS", self.run_tests),
            self.define("EMBREE_TUTORIALS_GLFW", False),
            self.define("EMBREE_IGNORE_CMAKE_CXX_FLAGS", True),
            self.define_from_variant("EMBREE_ISPC_SUPPORT", "ispc"),
        ]

        if spec.satisfies("target=x86_64:") or spec.satisfies("target=x86:"):
            # code selection and defines controlling namespace names are based on
            # defines controlled by compiler flags, so disable ISAs below compiler
            # flags chosen by spack
            args.append(self.define("EMBREE_ISA_SSE2", "sse4_2" not in spec.target))
            args.append(self.define("EMBREE_ISA_SSE42", "avx" not in spec.target))
            args.append(self.define("EMBREE_ISA_AVX", "avx2" not in spec.target))
            args.append(self.define("EMBREE_ISA_AVX2", "avx512" not in spec.target))

            # during the 3.12 cycle AVX512SKX was renamed to AVX512,
            # but for compatibility, the old name is still supported
            avx512_suffix = ""
            if spec.satisfies("@:3.12"):
                avx512_suffix = "SKX"
            args.append(self.define("EMBREE_ISA_AVX512" + avx512_suffix, True))
            if spec.satisfies("%gcc@:7"):
                # remove unsupported -mprefer-vector-width=256, otherwise copied
                # from common/cmake/gnu.cmake
                args.append(
                    self.define(
                        "FLAGS_AVX512" + avx512_suffix,
                        "-mavx512f -mavx512dq -mavx512cd -mavx512bw -mavx512vl"
                        " -mf16c -mavx2 -mfma -mlzcnt -mbmi -mbmi2",
                    )
                )

        return args
