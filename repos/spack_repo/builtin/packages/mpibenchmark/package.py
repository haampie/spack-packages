# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Mpibenchmark(AutotoolsPackage):
    """MadMPI benchmark.

    MadMPI benchmark is benchmark designed to assess the performance
    of MPI libraries using various metrics: point-to-point communications,
    collectives, communication/computation overlap, scalability with the
    number of requests, RMA, multi-threaded communications. It may be used to
    benchmark any MPI library.
    """

    homepage = "https://pm2.gitlabpages.inria.fr/mpibenchmark/"
    url = "https://pm2.gitlabpages.inria.fr/releases/mpibenchmark-0.5.tar.gz"
    list_url = "https://pm2.gitlabpages.inria.fr/releases/"
    git = "https://gitlab.inria.fr/pm2/pm2.git"


    variant("optimize", default=True, description="Build in optimized mode")
    variant("debug", default=False, description="Build in debug mode")
    variant("asan", default=False, description="Build with Address Sanitizer (ASAN)")


    build_directory = "build"

    @property
    def configure_directory(self) -> str:
        if "@master" in self.spec:
            return "mpibenchmark"
        else:
            return super().configure_directory

    def configure_args(self):
        config_args = [
            "--with-hwloc",  # always use hwloc in spack
            "--without-cuda",
            "--without-hip",
            *self.enable_or_disable("optimize"),
            *self.enable_or_disable("debug"),
            *self.enable_or_disable("asan"),
        ]
        return config_args

    def autoreconf(self, spec, prefix):
        with working_dir(self.configure_directory):
            Executable("./autogen.sh")()
