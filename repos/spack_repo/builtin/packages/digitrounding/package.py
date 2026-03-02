# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Digitrounding(CMakePackage):
    """Standalone version of Digit rounding compressor"""

    homepage = "https://github.com/disheng222/digitroundingZ"
    git = "https://github.com/disheng222/digitroundingZ"

    maintainers("robertu94")

    license("LGPL-3.0-or-later")




    variant("shared", default=True, description="build shared libraries")

    def cmake_args(self):
        args = []
        if self.spec.satisfies("+shared"):
            args.append("-DBUILD_SHARED_LIBS=ON")
        else:
            args.append("-DBUILD_SHARED_LIBS=OFF")
        return args
