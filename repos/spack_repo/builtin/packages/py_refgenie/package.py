# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyRefgenie(PythonPackage):
    """Refgenie manages storage, access, and transfer of reference genome resources."""

    homepage = "http://refgenie.databio.org"
    pypi = "refgenie/refgenie-0.12.1.tar.gz"

    license("BSD-2-Clause")

    version("0.12.1", sha256="cfd007ed0981e00d019deb49aaea896952341096494165cb8378488850eec451")


