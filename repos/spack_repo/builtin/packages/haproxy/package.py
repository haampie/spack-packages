# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class Haproxy(MakefilePackage):
    """
    HAProxy is a single-threaded, event-driven, non-blocking engine
    combining a very fast I/O layer with a priority-based scheduler.
    """

    homepage = "https://www.haproxy.org"
    url = "https://www.haproxy.org/download/2.1/src/haproxy-2.1.0.tar.gz"


    depends_on("c", type="build")  # generated

    def url_for_version(self, version):
        url = "https://www.haproxy.org/download/{0}/src/haproxy-{1}.tar.gz"
        return url.format(version.up_to(2), version)

    def build(self, spec, prefix):
        make("TARGET=generic", "PREFIX=" + prefix)

    def install(self, spec, prefix):
        install_tree(".", prefix)
