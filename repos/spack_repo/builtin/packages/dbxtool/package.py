# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class Dbxtool(MakefilePackage):
    """tool for managing dbx updates installed on a machine."""

    homepage = "https://github.com/rhboot/dbxtool"
    url = "https://github.com/rhboot/dbxtool/archive/dbxtool-8.tar.gz"



    depends_on("c", type="build")  # generated

    depends_on("efivar")
    depends_on("popt")

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        env.prepend_path("CPATH", self.spec["efivar"].prefix.include.efivar)

    def install(self, spec, prefix):
        make("PREFIX={0}".format(prefix), "install")
