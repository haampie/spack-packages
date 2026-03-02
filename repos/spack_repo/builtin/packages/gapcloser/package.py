# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.generic import Package

from spack.package import *


class Gapcloser(Package):
    """The GapCloser is designed to close the gaps emerging during the
    scaffolding process"""

    homepage = "https://sourceforge.net/projects/soapdenovo2/files/GapCloser/"
    url = "https://downloads.sourceforge.net/project/soapdenovo2/GapCloser/bin/r6/GapCloser-bin-v1.12-r6.tgz"


    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("GapCloser", prefix.bin)
