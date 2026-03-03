# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Libatasmart(AutotoolsPackage):
    """A small and lightweight parser library for ATA S.M.A.R.T. hard disk
    health monitoring."""

    homepage = "https://github.com/ebe-forks/libatasmart"
    url = "https://github.com/ebe-forks/libatasmart/archive/v0.19.tar.gz"



    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    def setup_run_environment(self, env: EnvironmentModifications) -> None:
        env.prepend_path("PATH", self.prefix.sbin)
