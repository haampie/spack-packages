# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Toml11(CMakePackage):
    """toml11 is a C++11 (or later) header-only toml parser/encoder depending
    only on C++ standard library."""

    homepage = "https://github.com/ToruNiina/toml11"
    url = "https://github.com/ToruNiina/toml11/archive/refs/tags/v3.7.1.tar.gz"




    variant(
        "cxx_std", default="11", description="C++ standard", values=("11", "14", "17"), multi=False
    )

    depends_on("cxx", type="build")  # generated

    @when("@3.8.0:")
    def cmake_args(self):
        args = [self.define_from_variant("CMAKE_CXX_STANDARD", "cxx_std")]
        return args
