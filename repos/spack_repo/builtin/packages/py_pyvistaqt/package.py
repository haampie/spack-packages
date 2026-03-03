# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyPyvistaqt(PythonPackage):
    """PyQT support for PyVista."""

    homepage = "https://github.com/pyvista/pyvistaqt"
    pypi = "pyvistaqt/pyvistaqt-0.5.0.tar.gz"

    license("MIT")

    version("0.5.0", sha256="f2358825d3c5f434760c13fdff5d3681b3cf36898e6e909c8a7934a8e6448f71")

