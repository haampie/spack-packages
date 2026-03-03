# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.meson import MesonPackage

from spack.package import *


class GlibNetworking(MesonPackage):
    """Network-related giomodules for glib."""

    homepage = "https://gitlab.gnome.org/GNOME/glib-networking"
    url = "https://github.com/GNOME/glib-networking/archive/2.66.0.tar.gz"


    depends_on("c", type="build")

    depends_on("gettext", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("glib")
    depends_on("gnutls")
    depends_on("gsettings-desktop-schemas")
    depends_on("libproxy")
