# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.go import GoPackage

from spack.package import *


class Etcd(GoPackage):
    """etcd is a distributed reliable key-value store for the most
    critical data of a distributed system"""

    homepage = "https://etcd.io/"
    url = "https://github.com/etcd-io/etcd/archive/v3.4.7.tar.gz"

    maintainers("alecbcs")

    license("Apache-2.0")

    version("3.6.5", sha256="96b2eabaf6da7dd21797152e7d1c1ce27da75926ae10e08a90b7ed0458287a4b")

    depends_on("gmake", type="build")
