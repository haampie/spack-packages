# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.generic import Package

from spack.package import *


class Cap3(Package):
    """CAP3 is DNA Sequence Assembly Program"""

    homepage = "http://seq.cs.iastate.edu/"
    url = "http://seq.cs.iastate.edu/CAP3/cap3.linux.x86_64.tar"


    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("cap3", prefix.bin)
        install("formcon", prefix.bin)
        mkdirp(prefix.doc)
        install("doc", prefix.doc)
        install("aceform", prefix.doc)
