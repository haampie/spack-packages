# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class AcpicaTools(MakefilePackage):
    """Debian packaging for the ACPICA user space tools"""

    homepage = "https://github.com/ahs3/acpica-tools"
    url = "https://github.com/ahs3/acpica-tools/archive/upstream/20200528.tar.gz"



    depends_on("flex", type="build")
    depends_on("bison", type="build")

    def install(self, spec, prefix):
        make(f"PREFIX={prefix}", "install")
