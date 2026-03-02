# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class Pbwt(MakefilePackage):
    """Implementation of Positional Burrows-Wheeler Transform for genetic data."""

    homepage = "https://github.com/richarddurbin/pbwt"
    url = "https://github.com/richarddurbin/pbwt/archive/refs/tags/v2.1.tar.gz"




    depends_on("c", type="build")
    depends_on("htslib")
    depends_on("zlib-api")
    depends_on("bzip2")
    depends_on("lzma")
    depends_on("curl")

    def patch(self):
        htslib = self.spec["htslib"]
        filter_file("^HTSDIR=../htslib$", f"HTSDIR={htslib.prefix}", "Makefile")
        filter_file(r"^CPPFLAGS=-I\$\(HTSDIR\)$", r"CPPFLAGS=-I$(HTSDIR)/include", "Makefile")
        filter_file(r"^HTSLIB=\$\(HTSDIR\)/libhts.a$", "HTSLIB=$(HTSDIR)/lib/libhts.a", "Makefile")
        filter_file(
            r"^LDLIBS=-lpthread \$\(HTSLIB\) -lz -lm -lbz2 -llzma -lcurl$",
            "LDLIBS=-lpthread $(HTSLIB) -lz -lm -lbz2 -llzma -lcurl -lcrypto -ldeflate",
            "Makefile",
        )

    @property
    def install_targets(self):
        return ["install", f"PREFIX={self.prefix.bin}"]
