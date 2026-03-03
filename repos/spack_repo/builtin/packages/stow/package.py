# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.gnu import GNUMirrorPackage

from spack.package import *


class Stow(AutotoolsPackage, GNUMirrorPackage):
    """GNU Stow: a symlink farm manager

    GNU Stow is a symlink farm manager which takes distinct
    packages of software and/or data located in separate
    directories on the filesystem, and makes them appear to be
    installed in the same place."""

    homepage = "https://www.gnu.org/software/stow/"
    gnu_mirror_path = "stow/stow-2.2.2.tar.bz2"


    depends_on("perl@5.6.1:")
