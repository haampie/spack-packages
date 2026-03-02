# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Orbit2(AutotoolsPackage):
    """ORBit is a fast and lightweight CORBA server."""

    homepage = "https://developer.gnome.org"
    url = "https://ftp.gnome.org/pub/GNOME/sources/ORBit2/2.14/ORBit2-2.14.19.tar.bz2"



    depends_on("c", type="build")  # generated

    depends_on("pkgconfig", type="build")
    depends_on("glib")
    depends_on("libidl")
