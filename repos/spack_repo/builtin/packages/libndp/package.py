# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Libndp(AutotoolsPackage):
    """Libndp - Library for Neighbor Discovery Protocol"""

    homepage = "http://www.libndp.org/"
    url = "https://github.com/jpirko/libndp/archive/v1.7.tar.gz"




    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
