# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import re
from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack.package import *
class Flex(AutotoolsPackage):
    """Flex is a tool for generating scanners."""
    executables = ["^flex$"]
    version("2.6.4", sha256="e87aae032bf07c26f85ac0ed3250998c37621d95f8bd748b31f15b33c45ee995")
    version("2.6.1", sha256="3c43f9e658e45e8aae3cf69fa11803d60550865f023852830d557c5f0623c13b")
    variant("nls", default=False, description="Enable native language support")
    variant("lex", default=True, description="Provide symlinks for lex and libl")
    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("bison", type="build")
