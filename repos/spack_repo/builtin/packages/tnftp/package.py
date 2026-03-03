# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Tnftp(AutotoolsPackage):
    """Tnftp is an FTP client. It is the default FTP client included with many
    BSD operating systems and Darwin"""

    homepage = "https://ftp.netbsd.org/pub/pkgsrc/current/pkgsrc/net/tnftpd/README.html"
    url = "https://cdn.netbsd.org/pub/NetBSD/misc/tnftp/tnftp-20230507.tar.gz"



    depends_on("c", type="build")  # generated

    depends_on("bison")
    depends_on("ncurses")
