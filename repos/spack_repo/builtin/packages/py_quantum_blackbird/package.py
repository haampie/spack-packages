# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyQuantumBlackbird(PythonPackage):
    """Blackbird is a quantum assembly language for continuous-variable quantum
    computation, that can be used to program Xanadu’s quantum photonics
    hardware and Strawberry Fields simulator.
    """

    homepage = "https://github.com/XanaduAI/blackbird"
    pypi = "quantum-blackbird/quantum-blackbird-0.5.0.tar.gz"

    license("Apache-2.0")

    version("0.5.0", sha256="065c73bf5263ce8f9b72dcd2b434f3bfbb471f0a6907c97a617ec0c8bde01db3")



