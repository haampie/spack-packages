# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.scons import SConsPackage

from spack.package import *


class Daos(SConsPackage):
    """The Distributed Asynchronous Object Storage (DAOS) is an open-source
    software-defined object store designed from the ground up for massively
    distributed Non Volatile Memory (NVM)."""

    homepage = "https://github.com/daos-stack/daos"
    git = "https://github.com/daos-stack/daos.git"
    maintainers("hyoklee")

    license("BSD-2-Clause-Patent")

    version("master", branch="master", submodules=True)
    version(
        "2.2.0", tag="v2.2.0", commit="d2a1f2790c946659c9398926254e6203fd957b7c", submodules=True
    )

    variant(
        "debug", default=False, description="Enable debugging info and strict compile warnings"
    )

    patch("0001-LIBPATH-fix-for-ALT_PREFIX.2.patch", when="@2.2.0:")


    def build_args(self, spec, prefix):
        args = ["PREFIX={0}".format(prefix), "USE_INSTALLED=all"]

        if spec.satisfies("+debug"):
            args.append("--debug=explain,findlibs,includes")

        # Construct ALT_PREFIX and make sure that '/usr' is last.
        alt_prefix = []
        for node in spec.traverse():
            alt_prefix.append(format(node.prefix))

        args.extend(
            [
                "WARNING_LEVEL=warning",
                "ALT_PREFIX=%s" % ":".join([str(elem) for elem in alt_prefix]),
                "GO_BIN={0}".format(spec["go"].prefix.bin) + "/go",
            ]
        )
        return args

    def install_args(self, spec, prefix):
        args = ["PREFIX={0}".format(prefix)]
        return args
