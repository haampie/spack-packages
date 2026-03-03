# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.packages.boost.package import Boost

from spack.package import *


class Libfive(CMakePackage):
    """libfive is a software library and set of tools for solid modeling."""

    homepage = "https://libfive.com"
    git = "https://github.com/libfive/libfive.git"

    license("GPL-2.0")

    # https://libfive.com/download/ recommends working from the master branch
    # and currently, all tags are from 2017:
    version("master", branch="master")



    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    # In case build of future git master fails, check raising the minimum Qt version

    variant("qt", default=True, description="Enable Studio UI(with Guile or Python)")
    variant("guile", default=True, description="Enable Guile support for Studio UI")
    variant("python", default=True, description="Enable Python support for Studio UI")

    variant(
        "packed_opcodes",
        default=False,
        description="packed opcodes breaks compatibility with saved f-reps!",
    )

    def cmake_args(self):
        if self.spec.satisfies("+qt~guile~python"):
            raise InstallError("The Qt-based Studio UI (+qt) needs +guile or +python!")

        return [
            self.define_from_variant("BUILD_STUDIO_APP", "qt"),
            self.define_from_variant("BUILD_GUILE_BINDINGS", "guile"),
            self.define_from_variant("BUILD_PYTHON_BINDINGS", "python"),
            self.define_from_variant("LIBFIVE_PACKED_OPCODES", "packed_opcodes"),
        ]
