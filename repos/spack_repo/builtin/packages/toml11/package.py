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



    version("4.0.2", sha256="d1bec1970d562d328065f2667b23f9745a271bf3900ca78e92b71a324b126070")
    version("4.0.1", sha256="96965cb00ca7757c611c169cd5a6fb15736eab1cd1c1a88aaa62ad9851d926aa")
    version("4.0.0", sha256="f3dc3095f22e38745a5d448ac629f69b7ee76d2b3e6d653e4ce021deb7f7266e")
    version("3.8.0", sha256="36ce64b09f9151b57ba1970f12a591006fcae17b751ba011314c1f5518e77bc7")
    version("3.7.1", sha256="afeaa9aa0416d4b6b2cd3897ca55d9317084103077b32a852247d8efd4cf6068")
    version("3.7.0", sha256="a0b6bec77c0e418eea7d270a4437510884f2fe8f61e7ab121729624f04c4b58e")
    version("3.6.1", sha256="ca4c390ed8da0d77ae6eca30e70ab0bf5cc92adfc1bc2f71a2066bc5656d8d96")
    version("3.6.0", sha256="39e8d651db346ae8c7e3b39d6338a37232b9af3bba36ade45b241bf105c2226c")

    variant(
        "cxx_std", default="11", description="C++ standard", values=("11", "14", "17"), multi=False
    )

    depends_on("cxx", type="build")  # generated

    @when("@3.8.0:")
    def cmake_args(self):
        args = [self.define_from_variant("CMAKE_CXX_STANDARD", "cxx_std")]
        return args
