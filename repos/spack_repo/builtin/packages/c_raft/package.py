# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class CRaft(AutotoolsPackage):
    """C implementation of the Raft consensus protocol."""

    homepage = "https://raft.readthedocs.io/en/latest/"
    git = "https://github.com/canonical/raft.git"
    url = "https://github.com/canonical/raft/archive/refs/tags/v0.17.1.tar.gz"

    maintainers("mdorier")



    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    variant("uv", default=True, description="Enable libuv support")

    depends_on("libuv@1.18.0:", when="+uv")

    def autoreconf(self, spec, prefix):
        autoreconf("--install", "--verbose", "--force")

    def configure_args(self):
        args = ["--disable-lz4"]
        args += self.enable_or_disable("uv")
        return args
