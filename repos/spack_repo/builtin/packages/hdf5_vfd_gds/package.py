# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.build_systems.cuda import CudaPackage

from spack.package import *


class Hdf5VfdGds(CMakePackage, CudaPackage):
    """This package enables GPU Direct Storage Virtual File Driver in HDF5."""

    # Package info
    homepage = "https://github.com/hpc-io/vfd-gds"
    url = "https://github.com/hpc-io/vfd-gds/archive/refs/tags/1.0.1.tar.gz"
    git = "https://github.com/hpc-io/vfd-gds.git"

    license("BSD-3-Clause-LBNL")

    # Versions

    depends_on("c", type="build")  # generated

    # Dependencies
    conflicts("~cuda")
    # Although cuFILE predates 11.7.0, it is not installed in a location the build
    # system can obtaion via `find_library`.  Packaging issues fixed in 11.7.1.
    conflicts("^cuda@:11.7.0")
    depends_on("cmake@3.12:", type="build")
    depends_on("hdf5@1.14.0:")

    def cmake_args(self):
        # CMake options
        args = [self.define("BUILD_TESTING", self.run_tests)]

        return args

    def setup_run_environment(self, env: EnvironmentModifications) -> None:
        env.prepend_path("HDF5_PLUGIN_PATH", self.spec.prefix.lib)
