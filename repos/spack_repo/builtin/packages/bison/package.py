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

    version("3.8.2", sha256="06c9e13bdf7eb24d4ceb6b59205a4f67c2c7e7213119644430fe82fbd14a0abb")
    version("3.8.1", sha256="ce318a47196155fb7c26912b513102f3d0e14757c2e495e34608757b61339c5c")
    version("3.8", sha256="d5d184d421aee15603939973a6b0f372f908edfb24c5bc740697497021ad9458")
    version("3.7.6", sha256="69dc0bb46ea8fc307d4ca1e0b61c8c355eb207d0b0c69f4f8462328e74d7b9ea")
    version("3.7.5", sha256="151cb5f12716e3fe93a27a317cd44878329659f275b342779bfaef4a526bbf70")

    variant("color", default=False, description="Enable experimental colored output", when="@3.4:")

    # https://lists.gnu.org/archive/html/bug-bison/2019-08/msg00008.html
    patch("parallel.patch", when="@3.4.2")

    provides("yacc")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("gettext", when="+color")
    depends_on("m4@1.4.6:", type=("build", "run"))
    depends_on("diffutils", type="build")

    # The NVIDIA compilers do not currently support some GNU builtins.
    # Detect this case and use the fallback path.
    patch("nvhpc-3.6.patch", when="@3.6.0:3.6 %nvhpc")
    patch("nvhpc-3.7.patch", when="@3.7.0:3.7 %nvhpc")

    conflicts("%intel@:14", when="@3.4.2:", msg="Intel 14 has immature C11 support")
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

