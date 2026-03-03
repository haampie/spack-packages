# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyRefgenconf(PythonPackage):
    """A Python object for standardized reference genome assets."""

    homepage = "https://github.com/refgenie/refgenconf"
    pypi = "refgenconf/refgenconf-0.12.2.tar.gz"

    license("BSD-2-Clause")

    version("0.12.2", sha256="6c9f9ecd8b91b4f75a535cfbdbdfb136f2dc9e9864142d07aa0352c61cf0cf78")


