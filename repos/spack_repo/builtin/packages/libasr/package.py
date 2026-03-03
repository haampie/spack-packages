# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Libasr(AutotoolsPackage):
    """libasr is a free, simple and portable asynchronous resolver library."""

    homepage = "https://github.com/OpenSMTPD/libasr"
    url = "https://github.com/OpenSMTPD/libasr/releases/download/1.0.4/libasr-1.0.4.tar.gz"



    depends_on("c", type="build")  # generated
