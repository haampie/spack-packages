# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.sourceware import SourcewarePackage

from spack.package import *


class Elfutils(AutotoolsPackage, SourcewarePackage):
    """elfutils is a collection of various binary tools such as
    eu-objdump, eu-readelf, and other utilities that allow you to
    inspect and manipulate ELF files. Refer to Table 5.Tools Included
    in elfutils for Red Hat Developer for a complete list of binary
    tools that are distributed with the Red Hat Developer Toolset
    version of elfutils."""

    homepage = "https://fedorahosted.org/elfutils/"
    sourceware_mirror_path = "elfutils/0.179/elfutils-0.179.tar.bz2"
    list_url = "https://sourceware.org/elfutils/ftp"
    list_depth = 1



    # Native language support from libintl.
    variant("nls", default=True, description="Enable Native Language Support.")
    variant("exeprefix", default=True, description="Add a prefix to generated executables.")

    # libdebuginfod support
    # NB: For 0.181 and newer, this enables _both_ the client and server
    variant(
        "debuginfod", default=False, description="Enable libdebuginfod support.", when="@0.179:"
    )

    # elfutils-0.185-static-inline.patch
    # elflint.c (buffer_left): Mark as 'inline' to avoid external linkage failure.

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("bzip2", type="link")
    depends_on("xz", type="link")
    depends_on("zlib-api", type="link")
    depends_on("zstd", type="link", when="@0.182:")

    depends_on("gettext", when="+nls")
    depends_on("iconv")
    depends_on("m4", type="build")
    depends_on("pkgconfig", type=("build", "link"))

    # debuginfod has extra dependencies
    with when("+debuginfod"), default_args(type="link"):
        depends_on("libmicrohttpd@0.9.33:")
        depends_on("libarchive@3.1.2:")
        depends_on("sqlite@3.7.17:")
        depends_on("curl@7.29.0:")
        depends_on("json-c@0.11:", when="@0.192:")


    # https://sourceware.org/bugzilla/show_bug.cgi?id=32684 elfutils on aarch64 requires
    # linux-headers 5.0 or higher, which is a dependency of glibc we don't model. So this is a more
    # strict constraint than necessary.

    provides("elf@1")

    # libarchive@:3.7 with iconv doesn't configure
    # see https://github.com/spack/spack/issues/36710
    # fix: https://github.com/libarchive/libarchive/pull/2611

    # https://sourceware.org/bugzilla/show_bug.cgi?id=24964

    # Elfutils uses -Wall and we don't want to fail the build over a
    # stray warning.
    # Install elf.h to include directory.
    # Provide location of libelf.so to match libelf.
