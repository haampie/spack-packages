# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Libevdev(AutotoolsPackage):
    """libevdev is a wrapper library for evdev devices. it moves the common
    tasks when dealing with evdev devices into a library and provides a
    library interface to the callers, thus avoiding erroneous ioctls, etc."""

    homepage = "https://cgit.freedesktop.org/libevdev"
    url = "https://github.com/whot/libevdev/archive/libevdev-1.5.4.tar.gz"



    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
