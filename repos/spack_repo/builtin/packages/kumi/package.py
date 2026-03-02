# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Kumi(CMakePackage):
    """KUMI - C++20 Tuple & Tuple-base Algorithms Library."""

    homepage = "https://jfalcou.github.io/kumi/"
    url = "https://github.com/jfalcou/kumi/archive/refs/tags/v3.0.tar.gz"
    maintainers("jfalcou")
    git = "https://github.com/jfalcou/kumi.git"

    license("BSL-1.0")

    version("main", branch="main")
    version("3.0", sha256="166b621e475935d2a3a195d13937a285060812c1fd7a95575a9c7b1dc425f2a1")

