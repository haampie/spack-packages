# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyReferencing(PythonPackage):
    """JSON Referencing + Python."""

    homepage = "https://referencing.readthedocs.io/"
    pypi = "referencing/referencing-0.35.1.tar.gz"

    maintainers("wdconinc")

    license("MIT", checked_by="wdconinc")

    version("0.36.2", sha256="df2e89862cd09deabbdba16944cc3f10feb6b3e6f18e902f7cc25609a34775aa")
    version("0.35.1", sha256="25b42124a6c8b632a425174f24087783efb348a6f1e0008e63cd4466fedf703c")


