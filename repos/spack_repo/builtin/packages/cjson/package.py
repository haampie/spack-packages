# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Cjson(CMakePackage):
    """Ultralightweight JSON parser in ANSI C."""

    homepage = "https://github.com/DaveGamble/cJSON"
    git = "https://github.com/DaveGamble/cJSON"
    url = "https://github.com/DaveGamble/cJSON/archive/refs/tags/v1.7.15.zip"


