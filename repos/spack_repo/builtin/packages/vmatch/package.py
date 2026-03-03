# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.generic import Package

from spack.package import *


class Vmatch(Package):
    """Vmatch is a versatile software tool for efficiently solving large scale
    sequence matching tasks"""

    homepage = "http://www.vmatch.de/"
    url = "http://www.vmatch.de/distributions/vmatch-2.3.0-Linux_x86_64-64bit.tar.gz"


    depends_on("c", type="build")  # generated

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, prefix.bin)
