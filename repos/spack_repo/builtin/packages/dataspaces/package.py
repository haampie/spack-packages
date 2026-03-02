# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


def is_string(x):
    """validate a string"""
    try:
        return isinstance(x, str)
    except ValueError:
        return False


class Dataspaces(AutotoolsPackage):
    """an extreme scale data management framework."""

    homepage = "http://www.dataspaces.org"
    url = "https://dataspaces.rdi2.rutgers.edu/downloads/dataspaces-1.6.2.tar.gz"



    variant("ptag", default="250", description="Cray UGNI protection tag", values=is_string)
    variant("mpi", default=True, description="Use MPI for collective communication")

    depends_on("c", type="build")

    depends_on("m4", type="build")
    depends_on("automake", type="build")
    depends_on("autoconf", type="build")

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./autogen.sh")

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        if self.spec.satisfies("+mpi"):
            env.set("CC", self.spec["mpi"].mpicc)
            env.set("FC", self.spec["mpi"].mpifc)

        env.set("CFLAGS", self.compiler.cc_pic_flag)

        if self.spec.satisfies("%gcc@10:"):
            env.set("FCFLAGS", "-fallow-argument-mismatch")

    def configure_args(self):
        args = []
        cookie = self.spec.variants["gni-cookie"].value
        ptag = self.spec.variants["ptag"].value
        if self.spec.satisfies("+dimes"):
            args.append("--enable-dimes")
        if self.spec.satisfies("+cray-drc"):
            args.append("--enable-drc")
        else:
            args.append("--with-gni-cookie=%s" % cookie)
            args.append("--with-gni-ptag=%s" % ptag)
        return args
