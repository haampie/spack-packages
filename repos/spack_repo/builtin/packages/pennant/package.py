# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class Pennant(MakefilePackage):
    """PENNANT is an unstructured mesh physics mini-app designed
    for advanced architecture research. It contains mesh data
    structures and a few physics algorithms adapted
    from the LANL rad-hydro code FLAG, and gives a sample of
    the typical memory access patterns of FLAG.
    """

    homepage = "https://github.com/lanl/PENNANT"
    url = "https://github.com/lanl/PENNANT/archive/pennant_v0.9.tar.gz"
    tags = ["proxy-app"]

    version("0.9", sha256="5fc07e64c246f8b1b552595a0868ba0042b7a2410aa844e7b510bc31e2512dd8")
    version("0.8", sha256="b07226b377c0e22c0f9a631be07ab28793c6d9a337a7a6eed2c7d4dc79f93f18")
    version("0.7", sha256="a6b7e76f7e68a693fd12ec338eaeb59430db9f12b69279b24f78724882684ae4")

    variant("openmp", default=True, description="Build with OpenMP support")
    variant("debug", default=False, description="Enable debug")

    depends_on("cxx", type="build")  # generated

    depends_on("mpi", when="+mpi")

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        debug = "-g"
        opt = "-O3"

        if self.compiler.name == "intel":
            opt += " -fast -fno-alias"

        makefile.filter("CXXFLAGS_DEBUG .*", "CXXFLAGS_DEBUG := {0}".format(debug))
        makefile.filter("CXXFLAGS_OPT .*", "CXXFLAGS_OPT := {0}".format(opt))
        makefile.filter(
            "CXXFLAGS_OPENMP .*", "CXXFLAGS_OPENMP := {0}".format(self.compiler.openmp_flag)
        )

        if "+mpi" in spec:
            makefile.filter("CXX .*", "CXX := {0}".format(spec["mpi"].mpicxx))
        else:
            makefile.filter("-DUSE_MPI", "#")
            makefile.filter("CXX .*", "CXX := c++")

        if "+openmp" not in spec:
            makefile.filter(".*CXXFLAGS_OPENMP.*", "#")

        if "+debug" in spec:
            makefile.filter(".*(CXXFLAGS_OPT).*", "CXXFLAGS := $(CXXFLAGS_DEBUG)")

    def install(self, spec, prefix):
        def install_dir(dirname):
            install_tree(dirname, join_path(prefix, dirname))

        mkdirp(prefix.bin)
        install("build/pennant", prefix.bin)
        install_dir("doc")
        install_dir("test")
        install("LICENSE", prefix)
        install("README", prefix)
