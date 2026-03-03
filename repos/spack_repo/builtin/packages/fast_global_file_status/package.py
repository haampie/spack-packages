# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class FastGlobalFileStatus(AutotoolsPackage):
    """provides a scalable mechanism to retrieve such information of a file,
    including its degree of distribution or replication and consistency."""

    homepage = "https://github.com/LLNL/FastGlobalFileStatus"
    url = "https://github.com/LLNL/FastGlobalFileStatus/files/2271592/fastglobalfilestatus-1.1.tar.gz"
    git = "https://github.com/LLNL/FastGlobalFileStatus.git"


    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("mrnet")
    # we depend on mpa@master for bug fixes since mpa 1.1
    depends_on("mount-point-attributes@1.1.1:")
    depends_on("mpi")
    depends_on("openssl")
    depends_on("elf")
    depends_on("autoconf", type="build", when="@master")
    depends_on("automake", type="build", when="@master")
    depends_on("libtool", type="build", when="@master")

    def configure_args(self):
        spec = self.spec
        args = [
            "--with-mpa=%s" % spec["mount-point-attributes"].prefix,
            "--with-mrnet=%s" % spec["mrnet"].prefix,
        ]
        return args
