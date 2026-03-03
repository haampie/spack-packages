# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Libapreq2(AutotoolsPackage):
    """httpd-apreq is subproject of the Apache HTTP Server Project
    whose committers develop and maintain the libapreq C library
    and its language bindings for Perl (contributions for additional
    language bindings are most welcome)."""

    homepage = "https://github.com/gitpan/libapreq2"
    url = "https://github.com/gitpan/libapreq2/archive/gitpan_version/2.13.tar.gz"



    depends_on("c", type="build")  # generated

    depends_on("apr")
    depends_on("apr-util")
    depends_on("httpd")
    depends_on("perl", type="build")
