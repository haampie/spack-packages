# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Metkit(CMakePackage):
    """Toolkit for manipulating and describing meteorological objects,
    implementing the MARS language and associated processing and semantics."""

    homepage = "https://github.com/ecmwf/metkit"
    git = "https://github.com/ecmwf/metkit.git"
    url = "https://github.com/ecmwf/metkit/archive/refs/tags/1.7.0.tar.gz"



    variant("tools", default=True, description="Build the command line tools")
    variant("grib", default=True, description="Enable support for GRIB format")
    variant("odb", default=False, description="Enable support for ODB data")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.12:", type="build")
    depends_on("ecbuild@3.4:", type="build")

    depends_on("eckit@1.16:")
    depends_on("eckit@1.21:", when="@1.10:")
    depends_on("eckit@:1.21", when="@:1.10")

    depends_on("eccodes@2.5:", when="+grib")
    depends_on("eccodes@2.27:", when="@1.10.2: +grib")

    depends_on("odc", when="+odb")

    conflicts(
        "+tools",
        when="~grib~odb",
        msg="None of the command line tools is built when both "
        "GRIB format and ODB data support are disabled",
    )

    def cmake_args(self):
        args = [
            self.define_from_variant("ENABLE_BUILD_TOOLS", "tools"),
            self.define_from_variant("ENABLE_GRIB", "grib"),
            self.define_from_variant("ENABLE_ODC", "odb"),
            # The tests download additional data (~4KB):
            self.define("ENABLE_TESTS", self.run_tests),
            # The library does not really implement support for BUFR format:
            self.define("ENABLE_BUFR", False),
            # The library does not really implement support for NetCDF format:
            self.define("ENABLE_NETCDF", False),
            # We do not need any experimental features:
            self.define("ENABLE_EXPERIMENTAL", False),
        ]
        return args
