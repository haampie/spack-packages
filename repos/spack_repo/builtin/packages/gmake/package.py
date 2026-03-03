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

