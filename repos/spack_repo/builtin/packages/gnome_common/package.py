# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class GnomeCommon(AutotoolsPackage):
    """Module containing various files needed to bootstrap GNOME modules
    built from git."""

    homepage = "https://gitlab.gnome.org/GNOME"
    url = "https://github.com/GNOME/gnome-common/archive/3.18.0.tar.gz"

    license("LGPL-2.1-or-later")

    version("3.18.0", sha256="8407fd8786a44c9ce47987de0906d9266492195df9251a089afaa06cc65c72d8")
    version("3.14.0", sha256="6ba2990ae52f54adf90626a8e04c41e58631870ed1b28088bb670cdc1eff22c7")
    version("3.12.0", sha256="b1dd2651900e701d3b732177ab633a35c8608e06c2ae78910130e5cbbda3b204")
    version("3.5.5", sha256="a8e0c6ffaa6224a417480bc95e05d0bff62bcb2a44c36f3581cc3a86edbe9626")
    version("3.4.0.1", sha256="8829fad03100358b69dfbab71287811c0fb3d76781efa01f931aaaf1fba0299c")

    depends_on("m4", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    def autoreconf(self, spec, prefix):
        autoreconf = which("autoreconf")
        autoreconf("-ifv")
