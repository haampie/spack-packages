# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class Usearch(MakefilePackage):
    """USEARCH is a unique sequence analysis tool with thousands of users
    world-wide.

    Note: A manual download is required for USEARCH when @:11.0.667.  Spack
    will search your current directory for the download file.  Alternatively,
    add this file to a mirror so that Spack can find it.  For instructions on
    how to set up a mirror, see
    https://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://www.drive5.com/usearch/"
    url = "https://github.com/rcedgar/usearch12/archive/refs/tags/v12.0-beta1.tar.gz"
    maintainers("snehring")

    build_directory = "src"

    version(
        "12.0-beta1", sha256="dbb06e4733801dab1c405616880261bd885ab171dfdb1d44e8ede48d739cdc43"
    )

    with when("@12:"):
        depends_on("ccache", type="build")

    patch("0001-Don-t-statically-link.patch", when="@12:")

    @property
    def manual_download(self):
        return self.spec.satisfies("@:11.0.667")

    def url_for_version(self, version):
        if version <= Version("11.0.667"):
            return "file://{0}/usearch{1}_i86linux32.gz".format(os.getcwd(), version)
        return super().url_for_version(version)

    def build(self, spec, prefix):
        if not self.spec.satisfies("@:11.0.667"):
            super().build(spec, prefix)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        if self.spec.satisfies("@:11.0.667"):
            install("usearch{0}_i86linux32".format(self.version), prefix.bin.usearch)
        else:
            install("bin/usearch{0}".format(self.version.up_to(1)), prefix.bin.usearch)
        set_executable(prefix.bin.usearch)
