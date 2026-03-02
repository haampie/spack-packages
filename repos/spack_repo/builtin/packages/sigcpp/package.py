# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Sigcpp(CMakePackage):
    """libsigc++ : The Typesafe Callback Framework for C++"""

    homepage = "https://libsigcplusplus.github.io/libsigcplusplus/"
    url = "https://github.com/libsigcplusplus/libsigcplusplus/archive/refs/tags/3.0.7.tar.gz"

    license("LGPL-3.0-only")

    version("3.6.0", sha256="bbe81e4f6d8acb41a9795525a38c0782751dbc4af3d78a9339f4a282e8a16c38")



    @run_after("install")
    def drop_doc(self):
        if self.spec.satisfies("~doc") and os.path.isdir(prefix.share):
            shutil.rmtree(prefix.share)

    @run_after("install")
    def fix_include(self):
        source = join_path(self.spec.prefix, "lib", "sigc++-3.0", "include", "sigc++config.h")
        target = join_path(self.spec.prefix, "include", "sigc++-3.0", "sigc++config.h")
        shutil.copy(source, target)
