# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.generic import Package

from spack.package import *


class Drill(Package):
    """
    Apache Drill is a distributed MPP query layer that supports SQL and
    alternative query languages against NoSQL and Hadoop data storage
    systems.
    """

    homepage = "https://drill.apache.org/"
    url = "https://dist.apache.org/repos/dist/release/drill/1.17.0/apache-drill-1.17.0.tar.gz"
    git = "https://github.com/apache/drill.git"



    # pom.xml, requireJavaVersion
    depends_on("java@8:", type="run")

    def install(self, spec, prefix):
        install_tree(".", prefix)
