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


    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
