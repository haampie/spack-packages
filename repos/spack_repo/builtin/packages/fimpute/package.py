# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.generic import Package

from spack.package import *


class Fimpute(Package):
    """FImpute uses an overlapping sliding window approach to efficiently
    exploit relationships or haplotype similarities between target and
    reference individuals."""

    homepage = "http://www.aps.uoguelph.ca/~msargol/fimpute/"
    url = "http://www.aps.uoguelph.ca/~msargol/fimpute/FImpute_Linux.zip"


    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("FImpute", prefix.bin)
