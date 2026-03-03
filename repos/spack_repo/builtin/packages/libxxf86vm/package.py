# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.xorg import XorgPackage

from spack.package import *


class Libxxf86vm(AutotoolsPackage, XorgPackage):
    """libXxf86vm - Extension library for the XFree86-VidMode X extension."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libXxf86vm"
    xorg_mirror_path = "lib/libXxf86vm-1.1.4.tar.gz"



    version("1.1.6", sha256="d2b4b1ec4eb833efca9981f19ed1078a8a73eed0bb3ca5563b64527ae8021e52")
    version("1.1.5", sha256="f3f1c29fef8accb0adbd854900c03c6c42f1804f2bc1e4f3ad7b2e1f3b878128")
    version("1.1.4", sha256="5108553c378a25688dcb57dca383664c36e293d60b1505815f67980ba9318a99")




    @property
    def libs(self):
        return find_libraries("libXxf86vm", self.prefix, shared=True, recursive=True)
