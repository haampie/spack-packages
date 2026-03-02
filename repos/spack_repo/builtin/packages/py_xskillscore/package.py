# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyXskillscore(PythonPackage):
    """Metrics for verifying forecasts."""

    homepage = "https://github.com/xarray-contrib/xskillscore"
    pypi = "xskillscore/xskillscore-0.0.24.tar.gz"



    with default_args(type="build"):
        depends_on("py-setuptools-scm-git-archive")

    with default_args(type=("build", "run")):
        depends_on("py-bottleneck")
        depends_on("py-cftime")
        depends_on("py-dask")
        depends_on("py-numba@0.52:")
        depends_on("py-numpy")
        depends_on("py-properscoring")
        depends_on("py-scikit-learn")
        depends_on("py-scipy")
        depends_on("py-toolz")
        depends_on("py-xarray@0.16.1:")
        depends_on("py-xhistogram@0.3.0:")
