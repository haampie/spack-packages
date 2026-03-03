# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.packages.boost.package import Boost

from spack.package import *


class Metall(CMakePackage):
    """A Persistent Memory Allocator For Data-Centric Analytics"""

    homepage = "https://github.com/LLNL/metall"
    git = "https://github.com/LLNL/metall.git"
    url = "https://github.com/LLNL/metall/archive/refs/tags/v0.20.tar.gz"


    tags = ["e4s"]



    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.12:", type="build")
    depends_on("boost@1.75:", type=("build", "link"))

    # googletest is required only for test
    # GCC is also required only for test (Metall is a header-only library)
    # Hint: Use 'spack install --test=root metall' or 'spack install --test=all metall'
    # to run test (adds a call to 'make test' to the build)
    depends_on("googletest %gcc@8.1.0:", type=("test"))

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, type=("build", "link"))

    def cmake_args(self):
        if self.run_tests:
            args = ["-DBUILD_TEST=ON", "-DSKIP_DOWNLOAD_GTEST=ON"]
            return args
        else:
            args = ["-DINSTALL_HEADER_ONLY=ON"]
            return args

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        # Configure the directories for test
        if self.run_tests:
            env.set("METALL_TEST_DIR", join_path(self.build_directory, "build_test"))

    # 'spack load metall' sets METALL_ROOT environmental variable
    def setup_run_environment(self, env: EnvironmentModifications) -> None:
        env.set("METALL_ROOT", self.prefix)
