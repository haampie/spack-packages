# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Simgrid(CMakePackage):
    """SimGrid is a framework for developing simulators of distributed
    applications targetting distributed platforms, which can in turn be
    used to prototype, evaluate and compare relevant platform configurations,
    system designs, and algorithmic approaches.
    """

    homepage = "https://simgrid.org/"
    url = "https://github.com/simgrid/simgrid/releases/download/v3.27/simgrid-3.27.tar.gz"
    git = "https://framagit.org/simgrid/simgrid.git"




    variant("doc", default=False, description="Build documentation")
    variant("smpi", default=True, description="SMPI provides MPI")
    variant("examples", default=False, description="Install examples")
    variant("mc", default=False, description="Model checker")
    variant("msg", default=False, description="Enables the old MSG interface")
    variant("python", default=False, description="Enables the Python bindings")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated
    extends("python", when="+python")  # generated

    # does not build correctly with some old compilers -> rely on packages
    depends_on("boost@:1.69.0", when="@:3.21")
    depends_on("boost+exception")

    conflicts(
        "%gcc@10:",
        when="@:3.23",
        msg="simgrid <= v3.23 cannot be built with gcc >= 10,"
        " please use an older release (e.g., %gcc@:9).",
    )

    conflicts("+msg", when="@3.34:", msg="MSG was removed from SimGrid v3.33.")

    # fix compilation with GCC 14 for v3.34
    patch(
        "https://github.com/simgrid/simgrid/commit/e4ecb51dcdf597fb02340d7855dafd0da9bd9018.patch?full_index=1",
        sha256="80cbe0eed635ff1864f0c2945763c8561b86c08c0c2b60d2ee5a57e1659ccc3d",
        when="@3.34",
    )

    def setup_dependent_package(self, module, dep_spec):
        if self.spec.satisfies("+smpi"):
            self.spec.smpicc = join_path(self.prefix.bin, "smpicc")
            self.spec.smpicxx = join_path(self.prefix.bin, "smpicxx")
            self.spec.smpifc = join_path(self.prefix.bin, "smpif90")
            self.spec.smpif77 = join_path(self.prefix.bin, "smpiff")

    def cmake_args(self):
        spec = self.spec
        args = [self.define_from_variant("enable_python", "python")]

        if not spec.satisfies("+doc"):
            args.append("-Denable_documentation=OFF")
        if spec.satisfies("+mc"):
            args.append("-Denable_model-checking=ON")
        if spec.satisfies("+msg"):
            args.append("-Denable_msg=ON")
        return args

    def install(self, spec, prefix):
        """Make the install targets"""
        with working_dir(self.build_directory):
            make("install")
            if spec.satisfies("+examples"):
                install_tree(join_path(self.build_directory, "examples"), prefix.examples)
