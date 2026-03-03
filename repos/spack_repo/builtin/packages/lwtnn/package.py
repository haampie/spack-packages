# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Lwtnn(CMakePackage):
    """Lightweight Trained Neural Network."""

    homepage = "https://github.com/lwtnn/lwtnn"
    url = "https://github.com/lwtnn/lwtnn/archive/refs/tags/v2.12.1.tar.gz"

    maintainers("haralmha")

    license("MIT")



    # https://github.com/lwtnn/lwtnn/issues/161
