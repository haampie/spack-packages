# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Harminv(AutotoolsPackage):
    """Harminv is a free program (and accompanying library) to solve the
    problem of harmonic inversion - given a discrete-time, finite-length
    signal that consists of a sum of finitely-many sinusoids (possibly
    exponentially decaying) in a given bandwidth, it determines the
    frequencies, decay constants, amplitudes, and phases of those sinusoids."""

    homepage = "https://github.com/NanoComp/harminv"
    url = "https://github.com/NanoComp/harminv/releases/download/v1.4.2/harminv-1.4.2.tar.gz"

    license("GPL-2.0-or-later")


    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")

    depends_on("blas")
    depends_on("lapack")

    def configure_args(self):
        spec = self.spec
        lapack = spec["lapack"].libs
        blas = spec["blas"].libs

        return [
            "--enable-shared",
            "--with-blas={0}".format(blas.ld_flags),
            "--with-lapack={0}".format(lapack.ld_flags),
        ]
