# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.gnu import GNUMirrorPackage

from spack.package import *


class Glibc(AutotoolsPackage, GNUMirrorPackage):
    """The GNU C Library provides many of the low-level components used
    directly by programs written in the C or C++ languages."""

    homepage = "https://www.gnu.org/software/libc/"
    gnu_mirror_path = "libc/glibc-2.33.tar.gz"
    git = "https://sourceware.org/git/glibc.git"

    build_directory = "build"
    tags = ["runtime"]


    provides("libc")
    provides("iconv")

    # Fix for newer GCC, related to -fno-common
    patch("locs.patch", when="@2.23:2.25")
    patch("locs-2.22.patch", when="@:2.22")

    # _obstack_compat symbol is not initialized

    # docs: install fails with "unknown command hsep / vsep"

    # rpc/types.h include issue, should be from local version, not system.

    # Avoid linking libgcc_eh

    # Use init_array (modified commit 4a531bb to unconditionally define
    # NO_CTORS_DTORS_SECTIONS)
    patch("4a531bb.patch", when="@:2.12")

    # make: mixed implicit and static pattern rules (trivial issue in docs)
    patch("32cf406.patch", when="@:2.10")
    # linker flag output regex

    # recent gcc + binutils have issues with the inline assembly in
    # the fallback code, so better to use the kernel-provided value.

    # include_next <limits.h> not working


    depends_on("texinfo", type="build")
    depends_on("gettext", type="build")
    depends_on("perl", type="build")
    # See 2d7ed98add14f75041499ac189696c9bd3d757fe
    # Since f2873d2da0ac9802e0b570e8e0b9e7e04a82bf55

    # From 2.29: generates locale/C-translit.h
    # before that it's a test dependency.


    with when("@master"):
        depends_on("libtool", type="build")

