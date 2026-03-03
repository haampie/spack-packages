# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class OphidiaIoServer(AutotoolsPackage):
    """In-memory IO server of the Ophidia framework"""

    homepage = "https://github.com/OphidiaBigData/ophidia-io-server"
    url = "https://github.com/OphidiaBigData/ophidia-io-server/archive/refs/tags/v1.7.3.tar.gz"
    maintainers("eldoo", "SoniaScard")
    version("1.7.3", sha256="a33f1010f72f163f103593d14e7b4480258e4c8f0094c792d2a19bcb88ef323f")



    def autoreconf(self, spec, prefix):
        autoreconf("--install", "--verbose", "--force")

    def configure_args(self):
        args = [
            "--with-plugin-path={0}".format(self.spec["ophidia-primitives"].prefix.lib),
            "--with-netcdf-path={0}".format(self.spec["netcdf-c"].prefix),
            "--enable-parallel-nc4",
        ]

        return args
