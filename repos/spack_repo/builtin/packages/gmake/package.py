# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack_repo.builtin.build_systems.generic import Package
from spack_repo.builtin.build_systems.gnu import GNUMirrorPackage

from spack.package import *


class Gmake(Package, GNUMirrorPackage):
    """GNU Make is a tool which controls the generation of executables and
    other non-source files of a program from the program's source files."""

    homepage = "https://www.gnu.org/software/make/"
    gnu_mirror_path = "make/make-4.2.1.tar.gz"

    # Stable releases
    version("4.4.1", sha256="dd16fb1d67bfab79a72f5e8390735c49e3e8e70b4945a15ab1f81ddb78658fb3")
    version("4.4", sha256="581f4d4e872da74b3941c874215898a7d35802f03732bdccee1d4a7979105d18")
    version("4.3", sha256="e05fdde47c5f7ca45cb697e973894ff4f5d79e13b750ed57d7b66d8defc78e19")
    version("4.2.1", sha256="e40b8f018c1da64edd1cc9a6fce5fa63b2e707e404e20cad91fbae337c98a5b7")
    version("4.1", sha256="9fc7a9783d3d2ea002aa1348f851875a2636116c433677453cc1d1acc3fc4d55")

    variant("guile", default=False, description="Support GNU Guile for embedded scripting")

    depends_on("c", type="build")

    with when("+guile"):
        depends_on("guile@:2.0", when="@:4.2")
        depends_on("guile@:3.0")
        depends_on("pkgconfig", type="build")


    # Avoid symlinking GNUMakefile to GNUMakefile
    build_directory = "spack-build"

    # See https://savannah.gnu.org/bugs/?57962

    tags = ["build-tools"]

    executables = ["^make$"]

