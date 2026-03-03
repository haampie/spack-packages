# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Haveged(AutotoolsPackage):
    """A Linux entropy source using the HAVEGE algorithm."""

    homepage = "https://github.com/jirka-h/haveged"
    url = "https://github.com/jirka-h/haveged/archive/v1.9.13/haveged-1.9.13.tar.gz"

    license("GPL-3.0-or-later")


    depends_on("c", type="build")  # generated
