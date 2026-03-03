# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PySarifTools(PythonPackage):
    """A set of command line tools and Python library for working with SARIF files."""

    homepage = "https://github.com/microsoft/sarif-tools"
    pypi = "sarif_tools/sarif_tools-3.0.5.tar.gz"

    version("3.0.5", sha256="52d09c101121231fb3489ad8c7af56896b8a95415cef726a6db5e7d74c6834d2")

    license("MIT")


