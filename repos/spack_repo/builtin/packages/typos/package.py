# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cargo import CargoPackage

from spack.package import *


class Typos(CargoPackage):
    """Source code spell checker."""

    homepage = "https://github.com/crate-ci/typos"
    url = "https://github.com/crate-ci/typos/archive/refs/tags/v1.28.4.tar.gz"



    depends_on("rust@1.87:", type="build", when="@1.39.1:")
    depends_on("rust@1.80:", type="build")

    build_directory = "crates/typos-cli"
