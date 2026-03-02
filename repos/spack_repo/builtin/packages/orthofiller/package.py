# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack_repo.builtin.build_systems.generic import Package

from spack.package import *


class Orthofiller(Package):
    """OrthoFiller: Identifying missing annotations for evolutionarily
    conserved genes."""

    homepage = "https://github.com/mpdunne/orthofiller/"
    url = "https://github.com/mpdunne/orthofiller/archive/1.1.4.tar.gz"



    depends_on("hmmer", type="run")
    depends_on("orthofinder", type="run")
    depends_on("python@2.7:", type="run")
    depends_on("py-biopython", type="run")
    depends_on("py-scipy", type="run")
    depends_on("r", type="run")
    depends_on("r-gamlss", type="run")
    depends_on("mafft", type="run")

    def install(self, spec, prefix):
        # orthofiller tests for common unix programs using man
        # runtime modules will quickly overflow the maximum MANPATH;
        # we change the man tests to use which instead, more reliable anyway
        filter_file('"man "', '"which "', "OrthoFiller.py", string=True)

        os.chmod("OrthoFiller.py", 0o755)
        mkdirp(prefix.bin)
        install("OrthoFiller.py", prefix.bin)
