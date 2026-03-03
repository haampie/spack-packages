# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyPyvista(PythonPackage):
    """Easier Pythonic interface to VTK."""

    homepage = "https://github.com/pyvista/pyvista"
    pypi = "pyvista/pyvista-0.32.1.tar.gz"

    # Requires optional trame dependency
    skip_modules = ["pyvista.ext", "pyvista.jupyter", "pyvista.trame"]

    maintainers("banesullivan")

    license("MIT")

    version("0.46.3", sha256="1f8e6e39516d24d93bc227f278841a0d72ec3722959f612cf4616d2720a8afe1")
    version("0.45.3", sha256="bca39f5ea17e45f40070ab45423dfd2c4fc81c33e0fb565bafded81c024fd04f")
    version("0.44.1", sha256="63976f5d57d151b3f7e1616dde40dcf56a66d1f37f6db067087fa9cc9667f512")
    version("0.42.3", sha256="00159cf0dea05c1ecfd1695c8c6ccfcfff71b0744c9997fc0276e661dc052351")
    version("0.37.0", sha256="d36a2c6d5f53f473ab6a9241669693acee7a5179394dc97595da14cc1de23141")
    version("0.32.1", sha256="585ac79524e351924730aff9b7207d6c5ac4175dbb5d33f7a9a2de22ae53dbf9")

    # https://github.com/pyvista/pyvista/releases/tag/v0.44.0

    # this is a virtual that can provide py-pillow as needed

    # https://github.com/pyvista/pyvista/issues/6857
    # 9.4.0 and 9.4.1 are not supported
    # https://github.com/pyvista/pyvista/issues/6731


    # Historical dependencies

    # '>=3.7.*' in python_requires: setuptools parser changed in v60 and errors.
