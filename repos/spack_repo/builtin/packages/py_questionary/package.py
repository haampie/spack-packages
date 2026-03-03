# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyQuestionary(PythonPackage):
    """Questionary is a Python library for effortlessly building
    pretty command line interfaces.
    """

    homepage = "https://github.com/tmbo/questionary"
    pypi = "questionary/questionary-1.9.0.tar.gz"

    maintainers("mathomp4")

    license("MIT")

    version("2.1.0", sha256="6302cdd645b19667d8f6e6634774e9538bfcd1aad9be287e743d96cacaf95587")
    version("1.9.0", sha256="a050fdbb81406cddca679a6f492c6272da90cb09988963817828f697cf091c55")


