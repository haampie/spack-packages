# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.maven import MavenPackage

from spack.package import *


class Orientdb(MavenPackage):
    """OrientDB is an Open Source Multi-Model NoSQL DBMS with the support
    of Native Graphs, Documents Full-Text, Reactivity, Geo-Spatial and Object
    Oriented concepts. It's written in Java and it's amazingly fast."""

    homepage = "https://orientdb.org"
    url = "https://github.com/orientechnologies/orientdb/archive/3.1.2.tar.gz"


    version("3.1.0", sha256="84f7ced66847fc5a7b987c701d60302e2aff63cdac2869941eee158251515b99")
