# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Ntirpc(CMakePackage):
    """New development on tirpc"""

    homepage = "https://github.com/nfs-ganesha/ntirpc"
    url = "https://github.com/nfs-ganesha/ntirpc/archive/v3.2.tar.gz"

    version("1.8.0", sha256="3bb642dccc8f2506b57a03b5d3358654f59f47b33fddfaa5a7330df4cf336f9f")
    version("1.7.3", sha256="8713ef095efc44df426bbd2b260ad457e5335bf3008fb97f01b0775c8042e54b")

    depends_on("c", type="build")  # generated

    depends_on("libnsl")
    depends_on("userspace-rcu")
