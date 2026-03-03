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


    variant("doc", default=True, description="Keep man files")

    depends_on("cxx", type="build")  # generated

    @run_after("install")
    def drop_doc(self):
        if self.spec.satisfies("~doc") and os.path.isdir(prefix.share):
            shutil.rmtree(prefix.share)

    @run_after("install")
    def fix_include(self):
        source = join_path(self.spec.prefix, "lib", "sigc++-3.0", "include", "sigc++config.h")
        target = join_path(self.spec.prefix, "include", "sigc++-3.0", "sigc++config.h")
        shutil.copy(source, target)
