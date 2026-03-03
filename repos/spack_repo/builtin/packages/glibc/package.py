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
    # _obstack_compat symbol is not initialized
    # docs: install fails with "unknown command hsep / vsep"
    # rpc/types.h include issue, should be from local version, not system.
    # Avoid linking libgcc_eh
    # Use init_array (modified commit 4a531bb to unconditionally define
    # NO_CTORS_DTORS_SECTIONS)
    # make: mixed implicit and static pattern rules (trivial issue in docs)
    # linker flag output regex
    # Use AT_RANDOM provided by the kernel instead of /dev/urandom;
    # recent gcc + binutils have issues with the inline assembly in
