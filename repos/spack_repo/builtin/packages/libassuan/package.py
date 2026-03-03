# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Libassuan(AutotoolsPackage):
    """Libassuan is a small library implementing the so-called Assuan protocol."""

    homepage = "https://gnupg.org/software/libassuan/index.html"
    url = "https://gnupg.org/ftp/gcrypt/libassuan/libassuan-2.4.5.tar.bz2"




    depends_on("c", type="build")  # generated

    depends_on("libgpg-error@1.17:")

    # error with multiple duplicate symbols in linker -- fixed in v3.0.2
    conflicts("platform=darwin", when="@3.0.0:3.0.1")

    def configure_args(self):
        return [
            "--enable-static",
            "--enable-shared",
            f"--with-libgpg-error-prefix={self.spec['libgpg-error'].prefix}",
        ]
