# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.build_systems.sourceforge import SourceforgePackage

from spack.package import *


class Ray(CMakePackage, SourceforgePackage):
    """Parallel genome assemblies for parallel DNA sequencing"""

    homepage = "https://denovoassembler.sourceforge.net/"
    sourceforge_mirror_path = "denovoassembler/Ray-2.3.1.tar.bz2"

    license("GPL-3.0-or-later")




    @run_after("build")
    def make(self):
        mkdirp(prefix.bin)
        make("PREFIX=%s" % prefix.bin)

    def install(self, spec, prefix):
        make("install")
