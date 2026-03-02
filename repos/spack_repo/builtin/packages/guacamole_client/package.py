# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.maven import MavenPackage

from spack.package import *


class GuacamoleClient(MavenPackage):
    """Apache Guacamole is a clientless remote desktop gateway. It
    supports standard protocols like VNC, RDP, and SSH."""

    homepage = "https://guacamole.apache.org/"
    url = "https://github.com/apache/guacamole-client/archive/1.2.0.tar.gz"

    license("Apache-2.0")

    version("1.5.5", sha256="ebbd3c0b73ddafbf6656d11324163f5b8d410f94b472791e6fa75fca13a5d30b")

    # remove usage of deprecated AccessController class, deprecated in java 17


    def build_args(self):
        # The file .spack_patched is flagged as an unapproved license
        return ["-Drat.numUnapprovedLicenses=1"]
