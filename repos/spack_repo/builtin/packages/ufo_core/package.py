# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class UfoCore(CMakePackage):
    """The UFO data processing framework is a C library suited to build general
    purpose streams data processing on heterogeneous architectures such as
    CPUs, GPUs or clusters. This package contains the run-time system and
    development files."""

    homepage = "https://ufo.kit.edu"
    url = "https://github.com/ufo-kit/ufo-core/archive/v0.14.0.tar.gz"



