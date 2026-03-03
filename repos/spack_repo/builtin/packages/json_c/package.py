# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class JsonC(CMakePackage):
    """A JSON implementation in C."""

    homepage = "https://github.com/json-c/json-c/wiki"
    url = "https://s3.amazonaws.com/json-c_releases/releases/json-c-0.15.tar.gz"


    version("0.14", sha256="b377de08c9b23ca3b37d9a9828107dff1de5ce208ff4ebb35005a794f30c6870")

    depends_on("c", type="build")

    depends_on("cmake@3.9:", when="@0.17:", type="build")

    def cmake_args(self):
        return [self.define("DISABLE_WERROR", True)]
