# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class Hardlink(MakefilePackage):
    """A simple command-line utility that implements directory hardlinks"""

    homepage = "https://github.com/selkhateeb/hardlink"
    url = "https://github.com/selkhateeb/hardlink/archive/v0.1.1.tar.gz"


    depends_on("c", type="build")  # generated

    def install(self, spec, prefix):
        make("PREFIX={0}".format(prefix), "install-homebrew")
