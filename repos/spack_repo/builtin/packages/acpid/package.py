# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Acpid(AutotoolsPackage):
    """ACPID used to try to handle events internally.  Rather than try to climb
    an ever-growing mountain, ACPID now lets YOU define what events to handle.
    Any event that publishes itself to /proc/acpi/event can be handled.
    ACPID reads a set of configuration files which define event->action pairs.
    This is how you make it do stuff. See the man page for details."""

    homepage = "http://www.tedfelix.com"
    url = "https://github.com/Distrotech/acpid/archive/2.0.28.tar.gz"

    license("GPL-2.0-or-later")

    version("2.0.25", sha256="947d2e4f9b2d61a728ce5d6139901f1b666dcef5e2a48833cb33d82895e261cf")
    version("2.0.24", sha256="05903901369c4ebea1d24e445b4a1d516dd3b07e7864cc752a2d09b4147e1985")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
