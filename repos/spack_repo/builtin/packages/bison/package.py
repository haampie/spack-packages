# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import sys

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.gnu import GNUMirrorPackage

from spack.package import *


class Bison(AutotoolsPackage, GNUMirrorPackage):
    """Bison is a general-purpose parser generator that converts
    an annotated context-free grammar into a deterministic LR or
    generalized LR (GLR) parser employing LALR(1) parser tables."""

    homepage = "https://www.gnu.org/software/bison/"
    gnu_mirror_path = "bison/bison-3.6.4.tar.gz"

    tags = ["build-tools"]

    executables = ["^bison$"]


    version("3.7", sha256="492ad61202de893ca21a99b621d63fa5389da58804ad79d3f226b8d04b803998")
    version("3.6.4", sha256="8183de64b5383f3634942c7b151bf2577f74273b2731574cdda8a8f3a0ab13e9")
    version("3.6.3", sha256="4b4c4943931e811f1073006ce3d8ee022a02b11b501e9cbf4def3613b24a3e63")
    version("3.6.2", sha256="e28ed3aad934de2d1df68be209ac0b454f7b6d3c3d6d01126e5cd2cbadba089a")

    variant("color", default=False, description="Enable experimental colored output", when="@3.4:")

    # https://lists.gnu.org/archive/html/bug-bison/2019-08/msg00008.html
    patch("parallel.patch", when="@3.4.2")

    provides("yacc")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("gettext", when="+color")
    depends_on("m4@1.4.6:", type=("build", "run"))

    # The NVIDIA compilers do not currently support some GNU builtins.
    # Detect this case and use the fallback path.

    conflicts(
        "%oneapi",
        msg=(
            "bison is likely miscompiled by oneapi compilers, "
            "see https://github.com/spack/spack/issues/37172"
        ),
    )

    if sys.platform == "darwin" and macos_version() >= Version("10.13"):
        patch("secure_snprintf.patch", level=0, when="@3.0.4")

    build_directory = "spack-build"

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"bison \(GNU Bison\)\s+(\S+)", output)
        return match.group(1) if match else None
