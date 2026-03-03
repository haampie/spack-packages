# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.xorg import XorgPackage

from spack.package import *


class Xrefresh(AutotoolsPackage, XorgPackage):
    """xrefresh - refresh all or part of an X screen."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xrefresh"
    xorg_mirror_path = "app/xrefresh-1.0.5.tar.gz"




