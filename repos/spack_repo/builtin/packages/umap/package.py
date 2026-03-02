# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Umap(CMakePackage):
    """Umap is a library that provides an mmap()-like interface to a
    simple, user-space page fault handler based on the userfaultfd Linux
    feature (starting with 4.3 linux kernel)."""

    homepage = "https://github.com/LLNL/umap"
    url = "https://github.com/LLNL/umap/archive/v2.1.0.tar.gz"
    git = "https://github.com/LLNL/umap.git"

    tags = ["e4s"]


    version("develop", branch="develop")
    version("2.1.1", sha256="6257e1ffd667a7d14e2061671328ccf7ecda27bc98fafb10f45502f967b1a115")
    version("2.1.0", sha256="dfdc5b717aecdbfbb0da22e8567b9f2ffbc3607000a31122bf7c5ab3b85cecd9")
    version("2.0.0", sha256="85c4bc68e8790393847a84eb54eaf6fc321acade382a399a2679d541b0e34150")
    version("1.0.0", sha256="c746de3fae5bfc5bbf36234d5e888ea45eeba374c26cd8b5a817d0c08e454ed5")

    variant("logging", default=False, description="Build with logging enabled.")
    variant("tests", default=False, description="Build test programs.")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def cmake_args(self):
        args = [
            self.define_from_variant("ENABLE_LOGGING", "logging"),
            self.define_from_variant("ENABLE_TESTS", "tests"),
        ]
        return args
