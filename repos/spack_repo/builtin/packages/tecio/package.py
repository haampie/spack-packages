# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Tecio(CMakePackage):
    """The TecIO library allows third-party applications to read and write
    Tecplot file format."""

    homepage = "https://www.tecplot.com/products/tecio-library/"
    url = "file://{}/tecio.tgz".format(os.getcwd())

    manual_download = True



    variant("mpi", default=False, description="Build tecio with mpi support.")

    depends_on("cmake@3.0.2:", type="build")

    depends_on("boost@1.69.0:+system", type="build")
    depends_on("mpi", when="+mpi")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    @property
    def root_cmakelists_dir(self):
        if self.spec.satisfies("+mpi"):
            return "teciompisrc"
        else:
            return "teciosrc"

    def install(self, spec, prefix):
        includes = [
            "StandardIntegralTypes.h",
            "TECIO.h",
            "tecio_Exports.h",
            "tecio.inc",
            "tecio.for",
            "tecio.f90",
        ]
        mkdirp(join_path(prefix, "include"))
        mkdirp(join_path(prefix, "lib"))
        mkdirp(join_path(prefix, "bin"))
        with working_dir(self.root_cmakelists_dir):
            for f in includes:
                install(f, prefix.include)
            install("tecio_license_agreement.txt", prefix)
        with working_dir(self.build_directory):
            install("szcombine", prefix.bin)
            if spec.satisfies("+mpi"):
                install("libteciompi.a", prefix.lib)
            else:
                install("libtecio.a", prefix.lib)
