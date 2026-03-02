# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class LibpressioTthresh(CMakePackage):
    """A tthresh implementation for libpressio"""

    homepage = "https://github.com/robertu94/libpressio_tthresh"
    url = "https://github.com/robertu94/libpressio_tthresh/archive/refs/tags/0.0.1.tar.gz"
    git = homepage

    maintainers("robertu94")

    license("LGPL-3.0-or-later")

    version("main", branch="main")
    version("0.0.8", sha256="c6590a965b0ff3e97db1bab8ddb6e552ad4f8142623d02323dc9598da9052309")
    version("0.0.1", sha256="9efcfa97a5a81e9c456f50b712adb806d9d2f2ed6039860615df0f2e9d96569e")

    depends_on("cxx", type="build")  # generated

    depends_on("eigen")
    depends_on("libpressio@0.99.4:", when="@0.0.8:")
    depends_on("libpressio@0.85.0:", when="@:0.0.5")
    depends_on("libpressio@0.88.0:", when="@0.0.6:")

    def cmake_args(self):
        args = []
        if self.run_tests:
            args.append("-DBUILD_TESTING=ON")
        else:
            args.append("-DBUILD_TESTING=OFF")
        return args

    @run_after("build")
    @on_package_attributes(run_tests=True)
    def check_test(self):
        make("test")
