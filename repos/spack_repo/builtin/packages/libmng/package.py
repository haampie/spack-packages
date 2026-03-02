# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems import autotools, cmake
from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Libmng(CMakePackage, AutotoolsPackage):
    """THE reference library for reading, displaying, writing
    and examining Multiple-Image Network Graphics.  MNG is the animation
    extension to the popular PNG image format."""

    homepage = "https://sourceforge.net/projects/libmng/"
    url = "https://downloads.sourceforge.net/project/libmng/libmng-devel/2.0.3/libmng-2.0.3.tar.gz"

    license("custom")




    build_system("cmake", "autotools", default="cmake")

    def patch(self):
        # jpeg requires stdio to be included before its headers.
        filter_file(r"^(\#include \<jpeglib\.h\>)", "#include<stdio.h>\n\\1", "libmng_types.h")


class CMakeBuilder(cmake.CMakeBuilder):
    def cmake_args(self):
        return ["-DWITH_LCMS2:BOOL=ON", "-DWITH_LCMS1:BOOL=OFF"]


class AutotoolsBuilder(autotools.AutotoolsBuilder):
    @run_before("configure")
    def clean_preconf(self):
        """Required, otherwise configure will crash as subdirectories have
        already been configured"""
        make("distclean")

    def configure_args(self):
        return ["--with-lcms2", "--without-lcms1"]
