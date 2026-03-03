# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Typhon(CMakePackage):
    """
    Typhon is a distributed communications library for unstructured mesh
    applications.
    """

    homepage = "https://github.com/UK-MAC/Typhon"
    url = "https://github.com/UK-MAC/Typhon/archive/v3.0.tar.gz"
    git = "https://github.com/UK-MAC/Typhon.git"



    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("mpi")

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        if self.spec.satisfies("%fj"):
            env.set("LDFLAGS", "--linkfortran")
