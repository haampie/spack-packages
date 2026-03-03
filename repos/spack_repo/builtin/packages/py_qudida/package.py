# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyQudida(PythonPackage):
    """QuDiDA is a micro library for very naive though quick
    pixel level image domain adaptation via scikit-learn
    transformers."""

    homepage = "https://github.com/arsenyinfo/qudida"
    pypi = "qudida/qudida-0.0.4.tar.gz"

    version("0.0.4", sha256="db198e2887ab0c9aa0023e565afbff41dfb76b361f85fd5e13f780d75ba18cc8")

