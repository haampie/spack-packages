# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyPywcs(PythonPackage):
    """pywcs is a set of routines for
    handling the FITS World Coordinate System (WCS) standard."""

    homepage = "https://github.com/spacetelescope/pywcs"
    url = "https://github.com/spacetelescope/pywcs/archive/1.12.1.tar.gz"

    version("1.12.1", sha256="efd4e0ea190e3a2521ebcde583452e126acdeac85cc8a9c78c8a96f10805b5e1")


