# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class Signify(MakefilePackage):
    """OpenBSD tool to signs and verify signatures on files."""

    homepage = "https://github.com/aperezdc/signify"
    url = "https://github.com/aperezdc/signify/archive/v23.tar.gz"


    depends_on("c", type="build")  # generated

    depends_on("libbsd@0.8:")

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        env.set("PREFIX", self.prefix)
