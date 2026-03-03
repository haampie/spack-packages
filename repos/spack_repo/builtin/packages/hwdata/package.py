# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Hwdata(AutotoolsPackage):
    """Hardware identification and configuration data."""

    homepage = "https://github.com/vcrhonek/hwdata"
    url = "https://github.com/vcrhonek/hwdata/archive/v0.337.tar.gz"



    def configure_args(self):
        return [f"--datarootdir={self.prefix.share}"]  # Will default to /usr/share if not set
