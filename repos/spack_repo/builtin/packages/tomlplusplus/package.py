# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Tomlplusplus(CMakePackage):
    """Header-only TOML config file parser and serializer for C++17"""

    homepage = "https://marzer.github.io/tomlplusplus/"
    url = "https://github.com/marzer/tomlplusplus/archive/refs/tags/v3.4.0.tar.gz"


    depends_on("cxx", type="build")
    depends_on("cmake@3.14:", type="build")
