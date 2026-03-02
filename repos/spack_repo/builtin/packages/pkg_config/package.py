# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class PkgConfig(AutotoolsPackage):
    """pkg-config is a helper tool used when compiling applications
    and libraries"""

    homepage = "https://www.freedesktop.org/wiki/Software/pkg-config/"
    # URL must remain http:// so Spack can bootstrap curl
    url = "https://pkgconfig.freedesktop.org/releases/pkg-config-0.29.2.tar.gz"

    license("GPL-2.0-only")

    version("0.29.2", sha256="6fc69c01688c9458a57eb9a1664c9aba372ccda420a02bf4429fe610e7e7d591")


    provides("pkgconfig")

    variant("internal_glib", default=True, description="Builds with internal glib")

    # The following patch is needed for gcc-6.1
    patch("g_date_strftime.patch", when="@:0.29.1")

    parallel = False

    tags = ["build-tools"]

    executables = ["^pkg-config$"]

