# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems import go
from spack_repo.builtin.build_systems.go import GoPackage

from spack.package import *


class GoBuilder(go.GoBuilder):
    @property
    def build_directory(self):
        return join_path(self.pkg.stage.source_path, "seqkit")


class Seqkit(GoPackage):
    """seqkit: a cross-platform and ultrafast toolkit for FASTA/Q file manipulation"""

    homepage = "https://bioinf.shenwei.me/seqkit/"
    url = "https://github.com/shenwei356/seqkit/archive/refs/tags/v2.4.0.tar.gz"

    license("MIT", checked_by="A-N-Other")

    version("2.10.0", sha256="5ebb8bd72b52a0b17064c7afda54a784bd71940fa28ca03114334af550734437")
    version("2.8.2", sha256="9cf1e744b785fa673af5a7a1ce2f96d52dc03e14b6537097df86aa6266204556")

    depends_on("go@1.17:", type="build")
