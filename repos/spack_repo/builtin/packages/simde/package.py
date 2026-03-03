# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.meson import MesonPackage

from spack.package import *


class Simde(MesonPackage):
    """The SIMDe header-only library provides fast, portable
    implementations of SIMD intrinsics on hardware which doesn't
    natively support them, such as calling SSE functions on ARM.
    There is no performance penalty if the hardware supports the
    native implementation (e.g., SSE/AVX runs at full speed on x86,
    NEON on ARM, etc.)."""

    homepage = "https://github.com/simd-everywhere/simde"
    url = "https://github.com/simd-everywhere/simde/archive/v0.6.0.tar.gz"
    git = "https://github.com/simd-everywhere/simde.git"


    depends_on("c", type="build")
    depends_on("cxx", type="build")

    patch("sve-gcc.patch", when="@0.6.0 %gcc")
    patch(
        "https://github.com/simd-everywhere/simde/commit/ef361ba5aba71e501f7c6db98a45c9b87d49f857.patch?full_index=1",
        sha256="b6c435dc335b22065334e9e49840a6f85dc7a5de1ff3e12096d0ae3bd14a3b09",
        when="@0.8.2",
    )
    conflicts("%gcc@8", when="target=a64fx", msg="Internal compiler error with gcc8 and a64fx")
