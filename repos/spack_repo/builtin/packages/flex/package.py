# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import re
from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack.package import *
class Flex(AutotoolsPackage):
    """Flex is a tool for generating scanners."""
    homepage = "https://github.com/westes/flex"
    url = "https://github.com/westes/flex/releases/download/v2.6.1/flex-2.6.1.tar.gz"
    tags = ["build-tools"]
    executables = ["^flex$"]
    # Avoid flex '2.6.2' (major bug)
    # See issue #2554; https://github.com/westes/flex/issues/113
    version("2.5.39", sha256="258d3c9c38cae05932fb470db58b6a288a361c448399e6bda2694ef72a76e7cd")
    depends_on("cxx", type="build")  # generated
    depends_on("bison", type="build")
    # Older tarballs don't come with a configure script and the patch for
    # 2.6.4 touches configure
    # 2.6.4 fails to compile with newer versions of gcc/glibc, see:
    # - https://github.com/spack/spack/issues/8152
    # - https://github.com/spack/spack/issues/6942
    # - https://github.com/westes/flex/issues/241
