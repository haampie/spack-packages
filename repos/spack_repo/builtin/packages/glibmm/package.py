# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Glibmm(AutotoolsPackage):
    """Glibmm is a C++ wrapper for the glib library."""

    homepage = "https://gitlab.gnome.org/GNOME/glibmm"
    url = "https://download-fallback.gnome.org/sources/glibmm/2.70/glibmm-2.70.0.tar.xz"

    # version('2.70.0', sha256='8008fd8aeddcc867a3f97f113de625f6e96ef98cf7860379813a9c0feffdb520')

    depends_on("cxx", type="build")  # generated

    depends_on("libsigcpp")
    # https://libsigcplusplus.github.io/libsigcplusplus/index.html
    # sigc++-2.0 and sigc++-3.0 are different parallel-installable ABIs:
    # libsigcpp@:2.99: are pre-releases of 3.0 & glibmm@:2.19 is not updated for @2.99:
    # The newer glibmm releases have dependencies which are not yet in spack:
    depends_on("libsigcpp@:2.9", when="@:2.19")
    depends_on("glib")
    depends_on("pkgconfig", type="build")

    patch("guint16_cast.patch", when="@2.19.3")

    def url_for_version(self, version):
        """Handle glibmm's version-based custom URLs."""
        url = "https://ftp.acc.umu.se/pub/GNOME/sources/glibmm"
        ext = ".tar.gz" if version < Version("2.28.2") else ".tar.xz"
        return url + "/%s/glibmm-%s%s" % (version.up_to(2), version, ext)
