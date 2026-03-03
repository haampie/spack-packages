# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Elfio(CMakePackage):
    """
    ELFIO is a header-only C++ library intended for reading and generating
    files in the ELF binary format.
    """

    homepage = "https://github.com/serge1/ELFIO"
    url = "https://github.com/serge1/ELFIO/releases/download/Release_3.9/elfio-3.9.tar.gz"



    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # note, 3.10 is required on master it seems
    depends_on("cmake@3.12:", when="@3.8:", type="build")
    depends_on("cmake@3.12.4:", when="@3.7", type="build")

    def cmake_args(self):
        return [
            self.define("ELFIO_BUILD_EXAMPLES", "OFF"),
            self.define("ELFIO_BUILD_TESTS", "OFF"),
        ]
