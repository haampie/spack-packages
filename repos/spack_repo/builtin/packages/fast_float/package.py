# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class FastFloat(CMakePackage):
    """Fast and exact implementation of the C++ from_chars functions for number
    types."""

    homepage = "https://github.com/fastfloat/fast_float"
    url = "https://github.com/fastfloat/fast_float/archive/refs/tags/v6.1.4.tar.gz"


    depends_on("cxx", type="build")
    depends_on("cmake@3.9:", type="build")

    depends_on("doctest", type="test")

    patch(
        "https://github.com/fastfloat/fast_float/commit/a7ed4e89c7444b5c8585453fc6d015c0efdf8654.patch?full_index=1",
        sha256="25561aa7db452da458fb0ae3075ef8e63ccab174ca8f5a6c79fb15cb342b3683",
        when="@:6.1.5",
    )

    def cmake_args(self):
        args = [self.define("FASTFLOAT_TEST", self.run_tests), self.define("SYSTEM_DOCTEST", True)]

        return args
