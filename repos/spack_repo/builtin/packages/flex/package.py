# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Flex(AutotoolsPackage):
    """Flex is a tool for generating scanners."""

    homepage = "https://github.com/westes/flex"
    url = "https://github.com/westes/flex/releases/download/v2.6.1/flex-2.6.1.tar.gz"

    tags = ["build-tools"]

    executables = ["^flex$"]


    version("2.6.4", sha256="e87aae032bf07c26f85ac0ed3250998c37621d95f8bd748b31f15b33c45ee995")
    version(
        "2.6.3",
        sha256="68b2742233e747c462f781462a2a1e299dc6207401dac8f0bbb316f48565c2aa",
        preferred=True,
    )
    # Avoid flex '2.6.2' (major bug)
    # See issue #2554; https://github.com/westes/flex/issues/113
    version("2.6.1", sha256="3c43f9e658e45e8aae3cf69fa11803d60550865f023852830d557c5f0623c13b")

    variant("nls", default=False, description="Enable native language support")
    variant("lex", default=True, description="Provide symlinks for lex and libl")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("bison", type="build")
    depends_on("gettext@0.19:", type="build", when="+nls")
    # Older tarballs don't come with a configure script and the patch for
    # 2.6.4 touches configure

    # 2.6.4 fails to compile with newer versions of gcc/glibc, see:
    # - https://github.com/spack/spack/issues/8152
    # - https://github.com/spack/spack/issues/6942
    # - https://github.com/westes/flex/issues/241

