# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Aspect(CMakePackage):
    """Parallel and extensible Finite Element code to simulate convection in the
    Earth's mantle and elsewhere."""

    homepage = "https://aspect.geodynamics.org"
    url = "https://github.com/geodynamics/aspect/releases/download/v2.1.0/aspect-2.1.0.tar.gz"
    git = "https://github.com/geodynamics/aspect.git"



    version("3.0.0", sha256="15c62575603f88f2061dafe06e37a47a2347d5242ea8328854304a0bd54b8888")
    version("2.5.0", sha256="31ea8da84b81ccc8225ca90f1f4687445e38f4ac9bab6ad5b57ba4e5e3567b3d")
    version("2.0.1", sha256="0bf5600c42afce9d39c1d285b0654ecfdeb0f30e9f3421651c95f54ca01ac165")
    version("2.0.0", sha256="d485c07f54248e824bdfa35f3eec8971b65e8b7114552ffa2c771bc0dede8cc0")

    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Debug", "Release"),
    )
    variant("gui", default=False, description="Enable the deal.II parameter GUI")
    variant("fpe", default=False, description="Enable floating point exception checks")
    variant("opendap", default=False, description="Enable OPeNDAP support for remote file access")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("dealii+p4est+trilinos+mpi")
    depends_on("dealii+p4est+trilinos+mpi+sundials", when="@3.0")
    depends_on("dealii-parameter-gui", when="+gui")
    depends_on("libdap4", when="+opendap")

    def cmake_args(self):
        return [self.define_from_variant("ASPECT_USE_FP_EXCEPTIONS", "fpe")]

    def setup_run_environment(self, env: EnvironmentModifications) -> None:
        env.set("Aspect_DIR", self.prefix)
