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

    maintainers("haampie")

    build_directory = "build"
    tags = ["runtime"]

    license("LGPL-2.1-or-later")

    provides("libc")
    provides("iconv")

    version("master", branch="master")
    version("2.43", sha256="e1e622cbd635019090fa23260e5d9ec219b12f97ae7ae02f033d4ae42cf2c004")
    version("2.39", sha256="97f84f3b7588cd54093a6f6389b0c1a81e70d99708d74963a2e3eab7c7dc942d")
    version("2.38", sha256="16e51e0455e288f03380b436e41d5927c60945abd86d0c9852b84be57dd6ed5e")
    version("2.37", sha256="e3a790c2f84eed5c5d569ed6172c253c607dd3962135437da413aa39aa4fd352")
    version("2.36", sha256="02efa6ffbbaf3e10e88f16818a862608d04b0ef838c66f6025ae120530792c9c")
    version("2.35", sha256="3e8e0c6195da8dfbd31d77c56fb8d99576fb855fafd47a9e0a895e51fd5942d4")
    version("2.34", sha256="255b7632746b5fdd478cb7b36bebd1ec1f92c2b552ee364c940f48eb38d07f62")
    version("2.25", sha256="ad984bac07844ecc222039d43bd5f1f1e1571590ea28045232ae3fa404cefc32")
    version("2.20", sha256="37e1de410d572a19b707b99786db9822bb4775e9d70517d88937ab12e6d6debc")
    version("2.19", sha256="18ad6db70724699d264add80b1f813630d0141cf3a3558b4e1a7c15f6beac796")
    version("2.6.1", sha256="6be7639ccad715d25eef560ce9d1637ef206fb9a162714f6ab8167fc0d971cae")
    version("2.5", sha256="16d3ac4e86eed75d85d80f1f214a6bd58d27f13590966b5ad0cc181df85a3493")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

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

    depends_on("texinfo", type="build")
    depends_on("gettext", type="build")
    depends_on("perl", type="build")
    depends_on("gawk", type="build")
    # See 2d7ed98add14f75041499ac189696c9bd3d757fe
    # Since f2873d2da0ac9802e0b570e8e0b9e7e04a82bf55

    # From 2.29: generates locale/C-translit.h
    # before that it's a test dependency.

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
