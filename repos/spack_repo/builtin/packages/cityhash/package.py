# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Cityhash(AutotoolsPackage):
    """CityHash, a family of hash functions for strings."""

    homepage = "https://github.com/google/cityhash"
    git = "https://github.com/google/cityhash.git"


    depends_on("cxx", type="build")  # generated

    def configure_args(self):
        return ["--enable-sse4.2"]
