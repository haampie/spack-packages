# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyScanpy(PythonPackage):
    """Scanpy is a scalable toolkit for analyzing single-cell
    gene expression data built jointly with anndata."""

    homepage = "https://scanpy.readthedocs.io/en/stable/"
    pypi = "scanpy/scanpy-1.9.1.tar.gz"

    license("BSD-3-Clause")

    version("1.9.1", sha256="00c9a83b649da7e0171c91e9a08cff632102faa760614fd05cd4d1dbba4eb541")

