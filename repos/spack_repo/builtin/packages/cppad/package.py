# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Cppad(CMakePackage):
    """A Package for Differentiation of C++ Algorithms."""

    homepage = "https://github.com/coin-or/CppAD"
    url = "https://github.com/coin-or/CppAD/archive/refs/tags/20240000.4.tar.gz"
    git = "https://github.com/coin-or/CppAD.git"



    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def cmake_args(self):
        # NOTE: This package does not obey CMAKE_INSTALL_PREFIX
        args = [
            self.define("cppad_prefix", self.prefix),
            self.define("CMAKE_BUILD_TYPE", "Release"),
            #
            # Installing documents sometimes fails.
            #
            # self.define("cmake_install_docdir", "share/cppad/doc"),
        ]

        return args
