# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyQuaternionic(PythonPackage):
    """Interpret numpy arrays as quaternionic arrays with numba acceleration"""

    homepage = "https://github.com/moble/quaternionic"
    pypi = "quaternionic/quaternionic-1.0.1.tar.gz"

    maintainers("nilsvu", "moble")

    license("MIT")

    version("1.0.1", sha256="ea69733d7311784963922bf08cc0c9c938b62fee2f91219f56544ff30658c10e")

