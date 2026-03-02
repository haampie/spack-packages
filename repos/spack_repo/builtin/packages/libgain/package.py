# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Libgain(AutotoolsPackage):
    """GaIn is intended to provide routines with a relatively simple interface
    for calculation of overlap, kinetic and 2,3 and 4 center Coulomb integrals
    over either Solid or Cubic Harmonics Gaussian basis sets."""

    homepage = "https://bigdft.org/"
    git = "https://gitlab.com/l_sim/bigdft-suite.git"

    license("GPL-3.0-only")



    def flag_handler(self, name, flags):
        flags.append(self.compiler.fc_pic_flag)
        return (None, None, flags)

    @property
    def libs(self):
        shared = self.spec.satisfies("+shared")
        return find_libraries("libGaIn", root=self.prefix, shared=shared, recursive=True)
