# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.generic import Package

from spack.package import *


class Zstr(Package):
    """This C++ header-only library enables the use of C++ standard
    iostreams to access ZLib-compressed streams."""

    homepage = "https://github.com/mateidavid/zstr"
    url = "https://github.com/mateidavid/zstr/archive/v1.0.4.tar.gz"

    maintainers("bvanessen")

    license("MIT")

    version("1.0.1", sha256="e17e67e00ede182504b3165cebd802420770541465d4ba41df1a15bf4c2a63b7")
    version("1.0.0", sha256="9f4fa8cb0d2cbba03dfe67900c48b6e75c8380d9263a0ac71d795f11e0224b96")

    depends_on("cxx", type="build")  # generated

    depends_on("zlib-api")

    def install(self, spec, prefix):
        """Make the install targets - Note that this package
        keeps it's headers in the src directory"""
        install_tree(join_path(self.stage.source_path, "src"), prefix.include)
