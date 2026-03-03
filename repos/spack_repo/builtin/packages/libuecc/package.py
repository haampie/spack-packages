# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Libuecc(CMakePackage):
    """libuecc is a very small generic-purpose Elliptic Curve Cryptography
    library compatible with Ed25519."""

    homepage = "https://github.com/fars/libuecc"
    url = "https://github.com/fars/libuecc/archive/v7.tar.gz"



    depends_on("c", type="build")  # generated
