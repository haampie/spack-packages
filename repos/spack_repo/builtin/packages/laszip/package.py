# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Laszip(CMakePackage):
    """Free and lossless LiDAR compression"""

    homepage = "https://laszip.org/"
    url = "https://github.com/LASzip/LASzip/releases/download/3.4.1/laszip-src-3.4.1.tar.gz"



    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
