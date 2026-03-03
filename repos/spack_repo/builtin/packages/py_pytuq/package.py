# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyPytuq(PythonPackage):
    """The Python Toolkit for Uncertainty Quantification (PyTUQ) is a
    Python-only collection of libraries and tools designed for quantifying
    uncertainty in computational models. PyTUQ offers a range of UQ
    functionalities, including Bayesian inference and linear regression
    methods, polynomial chaos expansions, and global sensitivity analysis
    methods. PyTUQ features advanced techniques for dimensionality
    reduction, such as SVD and Karhunen-Loeve expansions, along with
    various MCMC methods for calibration and inference. The toolkit also
    includes robust classes for multivariate random variables and
    integration techniques, making it a versatile resource for researchers
    and practitioners seeking to quantify uncertainty in their numerical
    predictions."""

    homepage = "https://sandialabs.github.io/pytuq/"
    pypi = "pytuq/pytuq-1.0.0.tar.gz"

    maintainers("bjdebus", "ksargsyan", "gregvw")

    license("BSD-3-Clause", checked_by="gregvw")

    version("1.0.0", sha256="1fc9fabf7bf183d38e104564e99d1950f7e2103baac5a13960c356173b9997ff")



    variant("nn", default=False, description="Enable neural network support")

