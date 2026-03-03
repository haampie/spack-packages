# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.generic import Package

from spack.package import *


class Tomcat(Package):
    """
    The Apache Tomcat software is an open source implementation of the
    Java Servlet, JavaServer Pages, Java Expression Language and Java
    WebSocket technologies.
    """

    homepage = "https://tomcat.apache.org/"
    url = (
        "https://archive.apache.org/dist/tomcat/tomcat-11/v11.0.0/bin/apache-tomcat-11.0.0.tar.gz"
    )


    # https://tomcat.apache.org/whichversion.html
    depends_on("java@8:", type="run", when="@9:")
    depends_on("java@11:", type="run", when="@10:")
    depends_on("java@17:", type="run", when="@11:")

    def url_for_version(self, version):
        return f"https://archive.apache.org/dist/tomcat/tomcat-{version.up_to(1)}/v{version}/bin/apache-tomcat-{version}.tar.gz"

    def install(self, spec, prefix):
        install_tree(".", prefix)
