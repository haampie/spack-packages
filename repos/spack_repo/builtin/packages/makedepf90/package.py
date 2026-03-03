# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Makedepf90(AutotoolsPackage):
    """Makedepf90 is a program for automatic creation of Makefile-style dependency lists for
    Fortran source code."""

    homepage = "https://salsa.debian.org/science-team/makedepf90"
    url = "https://deb.debian.org/debian/pool/main/m/makedepf90/makedepf90_3.0.1.orig.tar.xz"



    version("3.0.1", sha256="a11601ea14ad793f23fca9c7e7df694b6337f962ccc930d995d72e172edf29ee")

