# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class _3proxy(MakefilePackage):
    """3proxy - tiny free proxy server"""

    homepage = "https://3proxy.org"
    url = "https://github.com/z3APA3A/3proxy/archive/0.8.13.tar.gz"

    version("0.8.13", sha256="a6d3cf9dd264315fa6ec848f6fe6c9057db005ce4ca8ed1deb00f6e1c3900f88")


    def build(self, spec, prefix):
        make("-f", f"Makefile.{platform.system()}", f"CC={spack_cc}", f"LN={spack_cc}")

    def install(self, spec, prefix):
        make(
            "-f",
            f"Makefile.{platform.system()}",
            f"prefix={prefix}",
            f"CC={spack_cc}",
            f"LN={spack_cc}",
            "install",
        )
