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


    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # Fix for newer GCC, related to -fno-common
    patch("locs.patch", when="@2.23:2.25")
    patch("locs-2.22.patch", when="@:2.22")

    # _obstack_compat symbol is not initialized
    patch("39b1f61.patch", when="@:2.17")

    # docs: install fails with "unknown command hsep / vsep"
    patch("texi.patch", when="@2.16.0")

    # rpc/types.h include issue, should be from local version, not system.
    patch("fb21f89.patch", when="@:2.16")

    # Avoid linking libgcc_eh
    patch("95f5a9a-stub.patch", when="@:2.16")
    patch("95f5a9a-2.16.patch", when="@2.16")
    patch("95f5a9a-2.15.patch", when="@2.14:2.15")
    patch("95f5a9a-2.13.patch", when="@2.12:2.13")
    patch("95f5a9a-2.11.patch", when="@:2.11")

    # Use init_array (modified commit 4a531bb to unconditionally define
    # NO_CTORS_DTORS_SECTIONS)
    patch("4a531bb.patch", when="@:2.12")

    # make: mixed implicit and static pattern rules (trivial issue in docs)
    patch("32cf406.patch", when="@:2.10")

    # linker flag output regex
    patch("7c8a673.patch", when="@:2.9")

    # Use AT_RANDOM provided by the kernel instead of /dev/urandom;
    # recent gcc + binutils have issues with the inline assembly in
    # the fallback code, so better to use the kernel-provided value.
    patch("965cb60.patch", when="@2.8:2.9")
    patch("965cb60-2.7.patch", when="@2.7")
    patch("965cb60-2.6.patch", when="@2.6")
    patch("965cb60-2.5.patch", when="@2.5")

    # include_next <limits.h> not working
    patch("67fbfa5.patch", when="@:2.7")

    conflicts("musl")

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        if self.spec.satisfies("@:2.21"):
            env.append_flags("LDFLAGS", "-no-pie")
        if self.spec.satisfies("@:2.16"):
            # for some reason CPPFLAGS -U_FORTIFY_SOURCE is not enough, it has to be CFLAGS
            env.append_flags("CPPFLAGS", "-U_FORTIFY_SOURCE")
            env.append_flags("CFLAGS", "-O2 -g -fno-stack-protector -U_FORTIFY_SOURCE")
        if self.spec.satisfies("@:2.9"):
            # missing defines in elf.h after 965cb60.patch
            env.append_flags("CFLAGS", "-DAT_BASE_PLATFORM=24 -DAT_RANDOM=25")
        if self.spec.satisfies("@:2.6"):
            # change of defaults in gcc 10
            env.append_flags("CFLAGS", "-fcommon")
        if self.spec.satisfies("@2.5"):
            env.append_flags("CFLAGS", "-fgnu89-inline")

    def patch(self):
        # Support gmake >= 4
        filter_file(
            "    3.79* | 3.[89]*)",
            "    3.79* | 3.[89]* |  [4-9].* | [1-9][0-9]*)",
            "configure",
            string=True,
        )

        # Suport gcc >= 5
        filter_file(
            "3.4* | 4.[0-9]* )",
            "3.4* | 4.[0-9]* | [5-9].* | [1-9][0-9]*)",
            "configure",
            string=True,
        )

        # Support gcc >= 10
        filter_file(
            "4.[3-9].* | 4.[1-9][0-9].* | [5-9].* )",
            "4.[3-9].* | 4.[1-9][0-9].* | [5-9].* | [1-9][0-9]*)",
            "configure",
            string=True,
        )
        filter_file(
            "4.[4-9].* | 4.[1-9][0-9].* | [5-9].* )",
            "4.[4-9].* | 4.[1-9][0-9].* | [5-9].* | [1-9][0-9]*)",
            "configure",
            string=True,
        )

        # Support binutils
        filter_file(
            "2.1[3-9]*)",
            "2.1[3-9]*|2.1[0-9][0-9]*|2.[2-9][0-9]*|[3-9].*|[1-9][0-9]*)",
            "configure",
            string=True,
        )

    depends_on("bison", type="build")
    depends_on("texinfo", type="build")
    depends_on("gettext", type="build")
    depends_on("perl", type="build")
    depends_on("gawk", type="build")
    depends_on("sed", type="build")
    depends_on("gmake", type="build")

    # See 2d7ed98add14f75041499ac189696c9bd3d757fe
    depends_on("gmake@:4.3", type="build", when="@:2.36")
    # Since f2873d2da0ac9802e0b570e8e0b9e7e04a82bf55
    depends_on("gmake@4.0:", type="build", when="@2.28:")

    # From 2.29: generates locale/C-translit.h
    # before that it's a test dependency.
    depends_on("python@3.4:", type="build", when="@2.29:")

    depends_on("linux-headers")

    with when("@master"):
        depends_on("autoconf", type="build")
        depends_on("automake", type="build")
        depends_on("libtool", type="build")

    def configure_args(self):
        return [
            "--enable-kernel=4.4.1",
            "--with-headers={}".format(self.spec["linux-headers"].prefix.include),
            "--without-selinux",
        ]

    def build(self, spec, prefix):
        # 1. build just ld.so
        # 2. drop the rpath from ld.so -- otherwise it cannot be executed
        # 3. do the rest of the build that may directly run ld.so
        with working_dir(self.build_directory):
            make("-C", "..", f"objdir={os.getcwd()}", "lib")
            delete_rpath(join_path("elf", "ld.so"))
            make()

    @property
    def libs(self):
        return LibraryList([])

    @property
    def headers(self):
        return HeaderList([])
