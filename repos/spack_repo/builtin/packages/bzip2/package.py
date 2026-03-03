# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import sys

from spack_repo.builtin.build_systems.generic import Package
from spack_repo.builtin.build_systems.sourceware import SourcewarePackage

from spack.package import *


class Bzip2(Package, SourcewarePackage):
    """bzip2 is a freely available, patent free high-quality data
    compressor. It typically compresses files to within 10% to 15%
    of the best available techniques (the PPM family of statistical
    compressors), whilst being around twice as fast at compression
    and six times faster at decompression."""

    homepage = "https://sourceware.org/bzip2/"
    sourceware_mirror_path = "bzip2/bzip2-1.0.8.tar.gz"

    executables = [r"^bzip2$"]
    tags = ["windows"]

    version("1.0.7", sha256="e768a87c5b1a79511499beb41500bcc4caf203726fff46a6f5f9ad27fe08ab2b")
    version("1.0.6", sha256="a2848f34fcd5d6cf47def00461fcb528a0484d8edef8208d6d2e2909dc61d9cd")

    variant(
        "shared",
        default=(sys.platform != "win32"),
        description="Enables the build of shared libraries.",
    )
    variant("pic", default=False, description="Build static libraries with PIC")
    variant("debug", default=False, description="Enable debug symbols and disable optimization")

    # makefile.msc doesn't provide a shared recipe
    conflicts(
        "+shared",
        when="platform=windows",
        msg="Windows makefile has no recipe for shared builds, use ~shared.",
    )

    if sys.platform != "win32":
        depends_on("diffutils", type="build")

    depends_on("c", type="build")  # generated

    depends_on("gmake", type="build", when="platform=linux")
    depends_on("gmake", type="build", when="platform=darwin")

    # override default implementation
