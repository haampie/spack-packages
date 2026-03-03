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


    build_directory = "spack-build"




