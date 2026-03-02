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
    variant(
        "xar",
        default="libxml2",
        values=("libxml2", "expat"),
        description="What library to use for xar support",
    )
    variant(
        "crypto",
        default="openssl",
        values=("mbedtls", "nettle", "openssl"),
        description="What crypto library to use for mtree and xar hashes",
    )
    variant(
        "programs",
        values=any_combination_of("bsdtar", "bsdcpio", "bsdcat"),
        description="What executables to build",
    )
    variant("iconv", default=True, description="Support iconv")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("pkgconfig", type="build")

    depends_on("bzip2", when="compression=bz2lib")
    depends_on("lz4", when="compression=lz4")
    depends_on("lzo", when="compression=lzo2")




    # NOTE: `make check` is known to fail with the Intel compilers
    # The build test suite cannot be built with Intel

    def configure_args(self):
        spec = self.spec
        args = ["--without-libb2"]
        args += self.with_or_without("compression")
        args += self.with_or_without("crypto")
        args += self.with_or_without("xar")
        args += self.enable_or_disable("programs")

        if spec.satisfies("+iconv"):
            if spec["iconv"].name == "libiconv":
                args.append(f"--with-libiconv-prefix={spec['iconv'].prefix}")
            else:
                args.append("--without-libiconv-prefix")
        else:
            args.append("--without-iconv")

        return args
