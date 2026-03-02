# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Libemos(CMakePackage):
    """The Interpolation library (EMOSLIB) includes Interpolation software and
    BUFR & CREX encoding/decoding routines."""

    homepage = "https://software.ecmwf.int/wiki/display/EMOS/Emoslib"
    url = (
        "https://software.ecmwf.int/wiki/download/attachments/3473472/libemos-4.4.2-Source.tar.gz"
    )
    list_url = "https://software.ecmwf.int/wiki/display/EMOS/Releases"

    license("Apache-2.0")

    version("4.5.1", sha256="c982d9fd7dcd15c3a4d1e1115b90430928b660e17f73f7d4e360dd9f87f68c46")
    version("4.5.0", sha256="debe474603224c318f8ed4a1c209a4d1416807c594c3faa196059b2228824393")



    def cmake_args(self):
        return [
            self.define("ENABLE_ECCODE", True),
            self.define("CMAKE_Fortran_FLAGS", "-ffree-line-length-none"),
        ]
