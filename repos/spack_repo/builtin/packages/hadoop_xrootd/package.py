# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.maven import MavenPackage

from spack.package import *


class HadoopXrootd(MavenPackage):
    """Connector between Hadoop and XRootD protocols (EOS compatible)."""

    homepage = "https://gitlab.cern.ch/db/hadoop-xrootd"
    url = "https://lcgpackages.web.cern.ch/tarFiles/sources/hadoop-xrootd-v1.0.7.tar.gz"

    maintainers("haralmha")

    license("Apache-2.0")



    conflicts("%clang")

    def build_args(self):
        xrootd_prefix = self.spec["xrootd"].prefix
        return ["-Dxrootd.include.path={0}/include/xrootd".format(xrootd_prefix)]
