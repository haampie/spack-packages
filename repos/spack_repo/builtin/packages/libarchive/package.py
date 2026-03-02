# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Libarchive(AutotoolsPackage):
    """libarchive: C library and command-line tools for reading and
    writing tar, cpio, zip, ISO, and other archive formats."""

    homepage = "https://www.libarchive.org"
    url = "https://www.libarchive.org/downloads/libarchive-3.1.2.tar.gz"





    # TODO: BLAKE2 is missing
    variant(
        "compression",
        default="bz2lib,lz4,lzo2,lzma,zlib,zstd",
        values=("bz2lib", "lz4", "lzo2", "lzma", "zlib", "zstd"),
        multi=True,
        description="Supported compression",
    )






    # NOTE: `make check` is known to fail with the Intel compilers
    # The build test suite cannot be built with Intel

