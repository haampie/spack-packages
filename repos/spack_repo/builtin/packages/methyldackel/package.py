# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class Methyldackel(MakefilePackage):
    """MethylDackel (formerly named PileOMeth, which was a temporary name
    derived due to it using a PILEup to extract METHylation metrics) will
    process a coordinate-sorted and indexed BAM or CRAM file containing
    some form of BS-seq alignments and extract per-base methylation
    metrics from them.
    """

    homepage = "https://github.com/dpryan79/MethylDackel"
    url = "https://github.com/dpryan79/MethylDackel/archive/refs/tags/0.6.1.tar.gz"




    def edit(self, spec, prefix):
        filter_file(r"^prefix \?=.*$", "prefix = " + spec.prefix, "Makefile")
        filter_file(
            "$(LIBBIGWIG)",
            join_path(spec["libbigwig"].prefix.lib64, "libBigWig.a"),
            "Makefile",
            string=True,
        )
        filter_file(
            "-IlibBigWig",
            "-I" + spec["libbigwig"].prefix.include.libbigwig,
            "Makefile",
            string=True,
        )
