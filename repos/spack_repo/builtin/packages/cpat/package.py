# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class Cpat(PythonPackage):
    """CPAT is an alignment-free method to predict RNA coding potential using four sequence
    features"""

    homepage = "https://cpat.readthedocs.io/"
    pypi = "CPAT/CPAT-3.0.4.tar.gz"


    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pysam", type=("build", "run"))

    depends_on("r", type="run")
