# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.generic import Package

from spack.package import *


class Hive(Package):
    """
    The Apache Hive data warehouse software facilitates reading, writing,
    and managing large datasets residing in distributed storage using SQL.
    Structure can be projected onto data already in storage. A command line
    tool and JDBC driver are provided to connect users to Hive.
    """

    homepage = "https://hive.apache.org/"
    url = "https://www.apache.org/dist/hive/hive-3.1.2/apache-hive-3.1.2-bin.tar.gz"




    def install(self, spec, prefix):
        install_tree(".", prefix)
