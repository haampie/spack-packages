# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class UfoFilters(CMakePackage):
    """The UFO data processing framework is a C library suited to build general
    purpose streams data processing on heterogeneous architectures such as
    CPUs, GPUs or clusters. This package contains filter plugins."""

    homepage = "https://ufo.kit.edu"
    url = "https://github.com/ufo-kit/ufo-filters/archive/v0.14.1.tar.gz"


    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("ufo-core")
