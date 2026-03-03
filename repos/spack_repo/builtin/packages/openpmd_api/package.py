# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class OpenpmdApi(CMakePackage):
    """C++ & Python API for Scientific I/O"""

    homepage = "https://www.openPMD.org"
    url = "https://github.com/openPMD/openPMD-api/archive/0.17.0.tar.gz"
    git = "https://github.com/openPMD/openPMD-api.git"


    tags = ["e4s"]

    # C++17 up until here
    # C++14 up until here
    # C++11 up until here

    variant("shared", default=True, description="Build a shared version of the library")
    variant("mpi", default=True, description="Enable parallel I/O")
    variant("hdf5", default=True, description="Enable HDF5 support")
    variant("adios1", default=False, description="Enable ADIOS1 support", when="@:0.15")
    variant("adios2", default=True, description="Enable ADIOS2 support")
    variant("python", default=False, description="Enable Python bindings")


    with when("+hdf5"):
        depends_on("hdf5@1.8.13:")
        depends_on("hdf5@1.8.13: ~mpi", when="~mpi")
        depends_on("hdf5@1.8.13: +mpi", when="+mpi")
    with when("+adios1"):
        depends_on("adios@1.13.1: ~sz")
        depends_on("adios@1.13.1: ~mpi ~sz", when="~mpi")
        depends_on("adios@1.13.1: +mpi ~sz", when="+mpi")
    with when("+adios2"):
        depends_on("adios2@2.5.0:")
        depends_on("adios2@2.6.0:", when="@0.12.0:")
    with when("+python"):
        with default_args(type=("link", "test", "run")):
            depends_on("python@3.7:")
            depends_on("python@3.8:", when="@0.15.2:")
            depends_on("python@3.10:", when="@0.17.0:")


    # Fix breaking HDF5 1.12.0 API when build with legacy api options
    # https://github.com/openPMD/openPMD-api/pull/1012

    # CMake: Fix Python Install Directory

    # macOS AppleClang12 Fixes

    # forgot to bump version.hpp in 0.15.1

    # fix superbuild control in 0.16.0

    extends("python", when="+python")

    def cmake_args(self):
        spec = self.spec

        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            # variants
            self.define_from_variant("openPMD_USE_MPI", "mpi"),
            self.define_from_variant("openPMD_USE_HDF5", "hdf5"),
            self.define_from_variant("openPMD_USE_ADIOS1", "adios1"),
            self.define_from_variant("openPMD_USE_ADIOS2", "adios2"),
            self.define_from_variant("openPMD_USE_PYTHON", "python"),
            # tests and examples
            self.define("BUILD_TESTING", self.run_tests),
            self.define("BUILD_EXAMPLES", self.run_tests),
        ]

        # switch internally shipped third-party libraries for spack
        if spec.satisfies("+python"):
            args.append(self.define("openPMD_USE_INTERNAL_PYBIND11", False))

        args.append(self.define("openPMD_USE_INTERNAL_JSON", False))
        if spec.satisfies("@:0.14"):  # pre C++17 releases
            args.append(self.define("openPMD_USE_INTERNAL_VARIANT", False))
        if spec.satisfies("@0.15:"):
            args.append(self.define("openPMD_USE_INTERNAL_TOML11", False))

        if self.run_tests:
            args.append(self.define("openPMD_USE_INTERNAL_CATCH", False))

        return args

    def setup_run_environment(self, env: EnvironmentModifications) -> None:
        spec = self.spec
        # pre-load dependent CMake-PUBLIC header-only libs
        if spec.satisfies("@:0.14"):  # pre C++17 releases
            env.prepend_path("CMAKE_PREFIX_PATH", spec["mpark-variant"].prefix)
            env.prepend_path("CPATH", spec["mpark-variant"].prefix.include)

        # more deps searched in openPMDConfig.cmake
        if spec.satisfies("+mpi"):
            env.prepend_path("CMAKE_PREFIX_PATH", spec["mpi"].prefix)
        if spec.satisfies("+adios1"):
            env.prepend_path("CMAKE_PREFIX_PATH", spec["adios"].prefix)
            env.prepend_path("PATH", spec["adios"].prefix.bin)  # adios-config
        if spec.satisfies("+adios2"):
            env.prepend_path("CMAKE_PREFIX_PATH", spec["adios2"].prefix)
        if spec.satisfies("+hdf5"):
            env.prepend_path("CMAKE_PREFIX_PATH", spec["hdf5"].prefix)

    def setup_dependent_build_environment(
        self, env: EnvironmentModifications, dependent_spec: Spec
    ) -> None:
        spec = self.spec
        # pre-load dependent CMake-PUBLIC header-only libs
        if spec.satisfies("@:0.14"):  # pre C++17 releases
            env.prepend_path("CMAKE_PREFIX_PATH", spec["mpark-variant"].prefix)
            env.prepend_path("CPATH", spec["mpark-variant"].prefix.include)

    def check(self):
        """CTest checks after the build phase"""
        # note: for MPI-parallel tests, you can overwrite the standard CMake
        #       option -DMPIEXEC_EXECUTABLE=$(which jsrun) for jsrun or srun,
        #       etc.. Alternatively, you can also use -E <regex> to exclude
        #       parallel and MPI tests
        with working_dir(self.build_directory):
            # -j1 because individual tests create files that are read again by
            # later tests
            ctest("--output-on-failure", "-j1")

    def test_run_openpmd_ls(self):
        """Test if openpmd-ls runs correctly"""
        if self.spec.satisfies("@:0.11.0"):
            raise SkipTest("Package must be installed as version 0.11.1 or later")
        exe = which(join_path(self.prefix.bin, "openpmd-ls"))
        out = exe(output=str.split, error=str.split)
        assert str(self.spec.version) in out
