# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class GftlShared(CMakePackage):
    """
    Provides common gFTL containers of Fortran intrinsic types that
    are encountered frequently.
    """

    homepage = "https://github.com/Goddard-Fortran-Ecosystem/gFTL-shared"
    url = (
        "https://github.com/Goddard-Fortran-Ecosystem/gFTL-shared/archive/refs/tags/v1.5.0.tar.gz"
    )
    list_url = "https://github.com/Goddard-Fortran-Ecosystem/gFTL-shared/tags"
    git = "https://github.com/Goddard-Fortran-Ecosystem/gFTL-shared.git"


    version("main", branch="main")

    version("1.11.0", sha256="785f3ccae7a28a3060c2155d67754379991e60cde19b1b238f77ef68dc2ad022")

    depends_on("fortran", type="build")

    depends_on("m4", type=("build", "run"))

    depends_on("cmake@3.12:3", type="build", when="@:1.10")
    depends_on("cmake@3.24:", type="build", when="@1.11:")

    depends_on("gftl")

    # gftl-shared only works with the Fujitsu compiler from 1.8.0 onwards
    conflicts(
        "%fj",
        when="@:1.7.0",
        msg="gftl-shared only works with the Fujitsu compiler from 1.8.0 onwards",
    )

    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Debug", "Release"),
    )
