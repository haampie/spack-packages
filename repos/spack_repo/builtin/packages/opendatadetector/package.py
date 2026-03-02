# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Opendatadetector(CMakePackage):
    """Open Data Detector for High Energy Physics."""

    homepage = "https://gitlab.cern.ch/acts/OpenDataDetector.git"
    git = "https://gitlab.cern.ch/acts/OpenDataDetector.git"


    tags = ["hep"]


    version("v2", tag="v2", commit="7041ae086dff4ee4a8d5b65f5d9559acc6dbec47")
    version("v1", tag="v1", commit="81c43c6511723c13c15327479082d3dcfa1947c7")

    depends_on("c", type="build")  # because of DD4hep
    depends_on("cxx", type="build")

    depends_on("dd4hep")
    depends_on("root")
    depends_on("boost")

    def cmake_args(self):
        args = [self.define("CMAKE_CXX_STANDARD", self.spec["root"].variants["cxxstd"].value)]
        return args

    @property
    def libs(self):
        return find_libraries(
            "libOpenDataDetector*", root=self.prefix, shared=True, recursive=True
        )

    def setup_run_environment(self, env: EnvironmentModifications) -> None:
        env.set("OPENDATADETECTOR_DATA", join_path(self.prefix.share, "OpenDataDetector"))
        env.prepend_path("LD_LIBRARY_PATH", self.spec["opendatadetector"].libs.directories[0])
