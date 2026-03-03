# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class GuacamoleServer(AutotoolsPackage):
    """The guacamole-server package is a set of software which forms the
    basis of the Guacamole stack. It consists of guacd, libguac, and
    several protocol support libraries."""

    homepage = "https://guacamole.apache.org/"
    url = "https://github.com/apache/guacamole-server/archive/1.1.0.tar.gz"

    license("GPL-3.0-or-later")

    version("1.5.5", sha256="50430c0f0f3b92f2cd3e60436fab0cedee8c1a9f762696a666016347039c731e")


