# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.generic import Package

from spack.package import *


class UcscBedgraphtobigwig(Package):
    """Convert a bedGraph file to bigWig format."""

    homepage = "http://hgdownload.cse.ucsc.edu/admin/exe/"
    url = "https://hgdownload.cse.ucsc.edu/admin/exe/userApps.archive/userApps.v445.src.tgz"



    # This package has known issues installing with the latest MySQL because
    # MySQL removed the type my_bool, while mariadb didn't.
    # https://groups.google.com/a/soe.ucsc.edu/g/genome/c/mIT6fe9l99g
    conflicts("^mysql@8.0.0:")

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        env.set("MYSQLLIBS", "-lmysqlclient")
        env.set("L", "-lssl")
        env.set("BINDIR", "bin")

    def install(self, spec, prefix):
        with working_dir("kent/src/lib"):
            make()
        with working_dir("kent/src/htslib"):
            make()
        with working_dir("kent/src/jkOwnLib"):
            make()
        with working_dir("kent/src/hg/lib"):
            make()
        with working_dir("kent/src/hg/lib"):
            make()
        with working_dir("kent/src/utils/bedGraphToBigWig"):
            mkdirp(prefix.bin)
            mkdirp("bin")
            make()
            make("install")
            install("bin/bedGraphToBigWig", prefix.bin)
