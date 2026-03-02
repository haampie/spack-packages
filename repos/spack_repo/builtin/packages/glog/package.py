# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Glog(CMakePackage):
    """C++ implementation of the Google logging module."""

    homepage = "https://github.com/google/glog"
    url = "https://github.com/google/glog/archive/v0.3.5.tar.gz"

    license("BSD-3-Clause")

    version("0.7.1", sha256="00e4a87e87b7e7612f519a41e491f16623b12423620006f59f5688bfd8d13b08")
    version("0.7.0", sha256="375106b5976231b92e66879c1a92ce062923b9ae573c42b56ba28b112ee4cc11")


    depends_on("gflags")

    depends_on("cmake@3:", type="build")
    depends_on("cmake@3.16:", type="build", when="@0.6.0:")
    depends_on("cmake@3.22:", type="build", when="@0.7.0:")

    def cmake_args(self):
        return [self.define("BUILD_SHARED_LIBS", True)]
