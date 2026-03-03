# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cargo import CargoPackage

from spack.package import *


class Mergiraf(CargoPackage):
    """A syntax-aware git merge driver for a growing collection of programming
    languages and file formats.
    """

    homepage = "https://mergiraf.org/"
    url = "https://codeberg.org/mergiraf/mergiraf/archive/v0.6.0.tar.gz"
    list_url = "https://codeberg.org/mergiraf/mergiraf/releases"



    depends_on("rust@1.89:", type="build", when="@0.12:")
