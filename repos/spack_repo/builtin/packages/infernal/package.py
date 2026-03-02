# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Infernal(AutotoolsPackage):
    """Infernal (INFERence of RNA ALignment) is for searching DNA sequence
    databases for RNA structure and sequence similarities. It is an
    implementation of a special case of profile stochastic context-free
    grammars called covariance models (CMs)."""

    homepage = "http://eddylab.org/infernal/"
    url = "http://eddylab.org/infernal/infernal-1.1.2.tar.gz"

    version("1.1.5", sha256="ad4ddae02f924ca7c85bc8c4a79c9f875af8df96aeb726702fa985cbe752497f")


    depends_on("c", type="build")  # generated

    depends_on("mpi", when="+mpi")

    # v1.1.4 and below do not build on aarch64
    # https://github.com/EddyRivasLab/infernal/issues/30
    conflicts(
        "target=aarch64:",
        when="@:1.1.4",
        msg="infernal v1.1.4 and below are only available for x86_64 and PowerPC",
    )

    def configure_args(self):
        args = []
        if self.spec.satisfies("+mpi"):
            args.append("--enable-mpi")
        else:
            args.append("--disable-mpi")
        return args
