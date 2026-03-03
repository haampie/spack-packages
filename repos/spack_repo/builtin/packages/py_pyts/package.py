# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyPyts(PythonPackage):
    """pyts is a Python package for time series classification. It aims to make
    time series classification easily accessible by providing preprocessing and
    utility tools, and implementations of state-of-the-art algorithms. Most of
    these algorithms transform time series, thus pyts provides several tools to
    perform these transformations."""

    homepage = "https://github.com/johannfaouzi/pyts"
    pypi = "pyts/pyts-0.12.0.tar.gz"

    license("BSD-3-Clause")

    version("0.12.0", sha256="af85e09a14334cbe384318de6ca4379e9a30bf5bbd1aaf3a1c4a94872e9765b1")

