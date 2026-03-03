# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.gnu import GNUMirrorPackage

from spack.package import *


class Diffutils(AutotoolsPackage, GNUMirrorPackage):
    """GNU Diffutils is a package of several programs related to finding
    differences between files."""

    tags = ["core-packages"]

    executables = [r"^diff$"]

    homepage = "https://www.gnu.org/software/diffutils/"
    gnu_mirror_path = "diffutils/diffutils-3.7.tar.xz"

    version("3.12", sha256="7c8b7f9fc8609141fdea9cece85249d308624391ff61dedaf528fcb337727dfd")
    version("3.11", sha256="a73ef05fe37dd585f7d87068e4a0639760419f810138bd75c61ddaa1f9e2131e")
    version("3.10", sha256="90e5e93cc724e4ebe12ede80df1634063c7a855692685919bfe60b556c9bd09e")
    version("3.9", sha256="d80d3be90a201868de83d78dad3413ad88160cc53bcc36eb9eaf7c20dbf023f1")
    version("3.8", sha256="a6bdd7d1b31266d11c4f4de6c1b748d4607ab0231af5188fc2533d0ae2438fec")
    version("3.7", sha256="b3a7a6221c3dc916085f0d205abf6b8e1ba443d4dd965118da364a1dc1cb3a26")
    version("3.6", sha256="d621e8bdd4b573918c8145f7ae61817d1be9deb4c8d2328a65cea8e11d783bd6")


    build_directory = "spack-build"




