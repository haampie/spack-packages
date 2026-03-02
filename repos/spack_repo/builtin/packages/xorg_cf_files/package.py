# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.xorg import XorgPackage

from spack.package import *


class XorgCfFiles(AutotoolsPackage, XorgPackage):
    """The xorg-cf-files package contains the data files for the imake utility,
    defining the known settings for a wide variety of platforms (many of which
    have not been verified or tested in over a decade), and for many of the
    libraries formerly delivered in the X.Org monolithic releases."""

    homepage = "https://gitlab.freedesktop.org/xorg/util/cf"
    xorg_mirror_path = "util/xorg-cf-files-1.0.6.tar.gz"



    depends_on("pkgconfig", type="build")
