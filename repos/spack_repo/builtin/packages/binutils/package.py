# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import pathlib
import re

from spack_repo.builtin.build_systems import autotools
from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.gnu import GNUMirrorPackage

from spack.package import *


class Binutils(AutotoolsPackage, GNUMirrorPackage):
    """GNU binutils, which contain the linker, assembler, objdump and others"""

    homepage = "https://www.gnu.org/software/binutils/"
    gnu_mirror_path = "binutils/binutils-2.28.tar.bz2"


    tags = ["build-tools", "core-packages"]

    executables = ["^nm$", "^readelf$"]

    version("2.30", sha256="efeade848067e9a03f1918b1da0d37aaffa0b0127a06b5e9236229851d9d0c09")

    variant("plugins", default=True, description="enable plugins, needed for gold linker")
    # When you build ld.gold you automatically get ld, even when you add the
    # --disable-ld flag
    # The gold linker was removed in v2.44.
    variant("gold", default=False, when="@:2.43 +ld", description="Build the gold linker.")
    variant("libiberty", default=False, description="Also install libiberty.")
    variant("nls", default=False, description="Enable Native Language Support")
    variant("headers", default=False, description="Install extra headers (e.g. ELF)")
    variant("lto", default=False, description="Enable lto.")
    variant(
        "pgo",
        default=False,
        description="Build with profile-guided optimization (slow)",
        when="@2.37:",
    )
    variant("ld", default=False, description="Enable ld.")
    variant("gas", default=False, description="Enable as assembler.")
    variant("interwork", default=False, description="Enable interwork.")
    variant("gprofng", default=False, description="Enable gprofng.", when="@2.39:")
    variant(
        "libs",
        default="shared,static",
        values=("shared", "static"),
        multi=True,
        description="Build shared libs, static libs or both",
    )
    variant(
        "compress_debug_sections",
        default="zlib",
        values=(conditional("zstd", when="@2.40:"), "zlib", "none"),
        description="Enable debug section compression by default in ld, gas, gold.",
    )
    variant(
        "debuginfod",
        default=False,
        description="Enable debuginfod HTTP server support for readelf and objdump",
        when="@2.34:",
    )

    # 2.36 is missing some dependencies, this patch allows a parallel build.
    # https://sourceware.org/bugzilla/show_bug.cgi?id=27482
    patch("parallel-build-2.36.patch", when="@2.36")


    # compression libs for debug symbols.


    # pkg-config is used to locate zstd, libdebuginfod


    # PGO runs tests, which requires `runtest` from dejagnu

    # 2.34:2.40 needs makeinfo due to a bug, see:
    # https://sourceware.org/bugzilla/show_bug.cgi?id=25491
    # https://sourceware.org/bugzilla/show_bug.cgi?id=28909

    # gprofng requires bison

    with when("platform=darwin"):
        conflicts("+gold", msg="Binutils cannot build linkers on macOS")
        # 2.41 doesn't seem to have any problems.
        conflicts(
            "libs=shared",
            when="@2.37:2.40,2.42:",
            msg="https://github.com/spack/spack/issues/35817",
        )


    # When you build binutils with ~ld and +gas and load it in your PATH, you
    # may end up with incompatibilities between a potentially older system ld
    # and a recent assembler. For instance the linker on ubuntu 16.04 from
    # binutils 2.26 and the assembler from binutils 2.36.1 will result in:
    # "unable to initialize decompress status for section .debug_info"
    # when compiling with debug symbols on gcc.

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"GNU (nm|readelf).* (\S+)", output)
        return Version(match.group(2)).dotted.up_to(3) if match else None

        platform = self.spec.platform
        # grab the full binutils set of headers
        install_tree("include", extradir)
