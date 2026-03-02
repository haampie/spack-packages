# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.racket import RacketPackage

from spack.package import *


class RktZoLib(RacketPackage):
    """Libraries for handling zo files."""

    git = "ssh://git@github.com/racket/racket.git"



    depends_on("rkt-base@8.3:", type=("build", "run"), when="@1.3")

    racket_name = "zo-lib"
