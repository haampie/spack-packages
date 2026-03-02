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



    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./autogen.sh")

