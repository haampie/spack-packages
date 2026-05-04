# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.generic import Package

from spack.package import *


class ClingoBootstrapPgo(Package):
    """Resources for profile-guided optimization for clingo-bootstrap"""

    homepage = "https://github.com/spack/spack-clingo-pgo"
    git = "https://github.com/spack/spack-clingo-pgo.git"

    maintainers("haampie")

    version("1.0.2", commit="30bfa8a73fdf1d797c1d1d634aedfa48196c7aa8")
    version("1.0.1", commit="4326d65113f05b9030c36bf2886dbb0873013be3")
    version("1.0.0", commit="64bec625ae06b32b7f5f01bccf9d27d0432a018f")

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
        install_tree("share", prefix.share)
