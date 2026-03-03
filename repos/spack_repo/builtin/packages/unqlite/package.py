# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Unqlite(CMakePackage):
    """UnQLite is a in-process software library which implements a self-contained,
    serverless, zero-configuration, transactional NoSQL database engine."""

    homepage = "https://unqlite.org/"
    url = "https://github.com/symisc/unqlite/archive/v1.1.9.tar.gz"
    git = "https://github.com/symisc/unqlite.git"


    depends_on("cxx", type="build")  # generated
    depends_on("c", type="build")  # generated

    # This patch corresponds to https://github.com/symisc/unqlite/pull/99
    patch("0001-Removed-the-STATIC-key-word-to-enable-building-a-sha.patch", when="@1.1.9")

    def cmake_args(self):
        args = ["-DBUILD_SHARED_LIBS:BOOL=ON"]
        return args
