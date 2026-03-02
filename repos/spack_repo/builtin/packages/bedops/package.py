# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class Bedops(MakefilePackage):
    """BEDOPS is an open-source command-line toolkit that performs highly
    efficient and scalable Boolean and other set operations, statistical
    calculations, archiving, conversion and other management of genomic data of
    arbitrary scale."""

    homepage = "https://bedops.readthedocs.io"
    url = "https://github.com/bedops/bedops/archive/v2.4.39.tar.gz"

    maintainers("jacorvar")

    # Regarding the peculiar license() directive: bedops is licensed under the GPL v2,
    # but the bedops source bundles source for bzlip2, jansson, and zlib, and its
    # LICENSE has the licenses for those source codes appended.
    license("GPL-2.0-only AND bzip2-1.0.6 AND MIT AND Zlib")

    version("2.4.42", sha256="9daa0c098e37490a07f84664d2c61ff8909689995cf7e1673d259ccd4f1c453c")
    version("2.4.34", sha256="533a62a403130c048d3378e6a975b73ea88d156d4869556a6b6f58d90c52ed95")
    version("2.4.30", sha256="218e0e367aa79747b2f90341d640776eea17befc0fdc35b0cec3c6184098d462")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("python", type="run")

    @property
    def build_targets(self):
        # avoid static linking with glibc for all invocations
        return ["SFLAGS="]

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        make("install", "BINDIR=%s" % prefix.bin)
