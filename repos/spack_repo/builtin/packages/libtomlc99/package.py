# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.generic import Package

from spack.package import *


class Libtomlc99(Package):
    """TOML in c99; v0.4.0 compliant."""

    homepage = "https://github.com/cktan/tomlc99"
    git = "https://github.com/cktan/tomlc99.git"


    # Since there is no official versioning, yet, just use the date and prefix
    # with '0.' to make switching to proper versioning easier later.
    # Unfortunately, upstream Makefile does not build shared libaries, so use
    # local changes for now.
    # Does not build shared libraries.
    version("0.2019.03.06", commit="bd76f1276ee5f5df0eb064f1842af5ad1737cf1e")

    depends_on("c", type="build")  # generated
    depends_on("gmake", type="build")

    variant("debug", default=False, description="Build with debug enabled.")

    def install(self, spec, prefix):
        make_args = []
        if spec.satisfies("+debug"):
            make_args.append("DEBUG=1")

        make(*make_args)
        make("prefix={0}".format(prefix), "install")
