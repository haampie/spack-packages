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




    depends_on("gmake", type="build")
