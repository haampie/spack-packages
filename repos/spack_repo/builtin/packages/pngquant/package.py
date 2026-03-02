# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Pngquant(AutotoolsPackage):
    """
    pngquant is a command-line utility and a library for lossy compression of
    PNG images.
    """

    homepage = "https://pngquant.org/"
    url = "https://pngquant.org/pngquant-2.12.5-src.tar.gz"

    license("GPL-3.0-or-later")



