# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Libevpath(CMakePackage):
    """EVpath is an event transport middleware layer designed to allow
    for the easy implementation of overlay networks, with
    active data processing, routing and management at all points
    in the overlay. EVPath is designed for high performance systems.
    """

    homepage = "https://github.com/GTkorvo/evpath"
    url = "https://github.com/GTkorvo/evpath/archive/v4.1.1.tar.gz"
    git = "https://github.com/GTkorvo/evpath.git"


    variant("enet_transport", default=False, description="Build an ENET transport for EVpath")

    depends_on("c", type="build")  # generated

    depends_on("gtkorvo-enet", when="@4.4.0: +enet_transport")
    depends_on("gtkorvo-enet@1.3.13", when="@:4.2.4 +enet_transport")
    depends_on("libffs")

    def cmake_args(self):
        args = ["-DTARGET_CNL=1"]
        if self.spec.satisfies("@4.4.0:"):
            args.append("-DBUILD_SHARED_LIBS=OFF")
        else:
            args.append("-DENABLE_BUILD_STATIC=STATIC")

        if self.run_tests:
            args.append("-DENABLE_TESTING=1")
        else:
            args.append("-DENABLE_TESTING=0")

        return args
