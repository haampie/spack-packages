# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Addrwatch(AutotoolsPackage):
    """A tool similar to arpwatch for IPv4/IPv6 and ethernet address
    pairing monitoring."""

    homepage = "https://github.com/fln/addrwatch"
    url = "https://github.com/fln/addrwatch/releases/download/v1.0.2/addrwatch-1.0.2.tar.gz"




    depends_on("libevent")
    depends_on("libpcap")
