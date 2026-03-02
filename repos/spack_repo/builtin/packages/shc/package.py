# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Shc(AutotoolsPackage):
    """A generic shell script compiler. Shc takes a script,
    which is specified on the command line and produces C
    source code. The generated source code is then compiled
    and linked to produce a stripped binary executable."""

    homepage = "https://neurobin.org/projects/softwares/unix/shc/"
    url = "https://github.com/neurobin/shc/archive/refs/tags/4.0.3.tar.gz"

    license("GPL-3.0-or-later")

    version("3.9.8", sha256="8b31e1f2ceef3404217b9578fa250a8a424f3eaf03359dd7951cd635c889ad79")
