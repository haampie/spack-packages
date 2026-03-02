# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Metaphysicl(AutotoolsPackage):
    """Metaprogramming and operator-overloaded classes for
    numerical simulations."""

    homepage = "https://github.com/roystgnr/MetaPhysicL"
    url = "https://github.com/roystgnr/MetaPhysicL/archive/v0.2.0.tar.gz"

    license("LGPL-2.1-or-later")

    version("0.6.0", sha256="a1b8469de17ad9960b4c99a9dbe2db46b7da50f97c811467efce470585d3f7f2")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
