# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Sigio(CMakePackage):
    """The SIGIO library provides an Application Program Interface for performing
    I/O on the sigma restart file of the NOAA global spectral model.

    This is part of the NCEPLIBS project."""

    homepage = "https://noaa-emc.github.io/NCEPLIBS-sigio"
    url = "https://github.com/NOAA-EMC/NCEPLIBS-sigio/archive/refs/tags/v2.3.2.tar.gz"
    git = "https://github.com/NOAA-EMC/NCEPLIBS-sigio"



    depends_on("fortran", type="build")

    conflicts("%oneapi", when="@:2.3.2", msg="Requires @2.3.3: for Intel OneAPI")

    def cmake_args(self):
        args = [self.define("ENABLE_TESTS", self.run_tests)]
        return args

    def setup_run_environment(self, env: EnvironmentModifications) -> None:
        lib = find_libraries("libsigio", root=self.prefix, shared=False, recursive=True)
        # Only one library version, but still need to set _4 to make NCO happy
        for suffix in ("4", ""):
            env.set("SIGIO_LIB" + suffix, lib[0])
            env.set("SIGIO_INC" + suffix, join_path(self.prefix, "include"))

    def flag_handler(self, name, flags):
        if self.spec.satisfies("%fj"):
            if name == "fflags":
                flags.append("-Free")
        return (None, None, flags)

    def check(self):
        with working_dir(self.build_directory):
            make("test")
