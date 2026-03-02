# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class CAres(CMakePackage):
    """c-ares: A C library for asynchronous DNS requests"""

    homepage = "https://c-ares.haxx.se"
    url = "https://github.com/c-ares/c-ares/archive/cares-1_15_0.tar.gz"
    git = "https://github.com/c-ares/c-ares.git"

    license("MIT")

    version("master", branch="master")
    version("1.28.1", sha256="e520d971415e48e607819c2f4b377b0aa69044ef6619160bb41bdba15ab4d545")

    depends_on("cxx", type="build")  # generated

    def url_for_version(self, version):
        url = "https://github.com/c-ares/c-ares/archive/cares-{0}.tar.gz"
        return url.format(version.underscored)

    @property
    def libs(self):
        return find_libraries(["libcares"], root=self.prefix, recursive=True)
