# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.xorg import XorgPackage

from spack.package import *


class Xrx(AutotoolsPackage, XorgPackage):
    """The remote execution (RX) service specifies a MIME format for invoking
    applications remotely, for example via a World Wide Web browser.  This
    RX format specifies a syntax for listing network services required by
    the application, for example an X display server.  The requesting Web
    browser must identify specific instances of the services in the request
    to invoke the application."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xrx"
    xorg_mirror_path = "app/xrx-1.0.4.tar.gz"




