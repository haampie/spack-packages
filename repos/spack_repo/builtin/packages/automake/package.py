# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.gnu import GNUMirrorPackage

from spack.package import *


class Automake(AutotoolsPackage, GNUMirrorPackage):
    """Automake -- make file builder part of autotools"""

    homepage = "https://www.gnu.org/software/automake/"
    gnu_mirror_path = "automake/automake-1.15.tar.gz"

    executables = ["^automake$"]

    tags = ["build-tools"]

    version("1.18.1", sha256="63e585246d0fc8772dffdee0724f2f988146d1a3f1c756a3dc5cfbefa3c01915")
    version("1.16.5", sha256="07bd24ad08a64bc17250ce09ec56e921d6343903943e99ccf63bbf0705e34605")


    build_directory = "spack-build"

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"GNU automake\)\s+(\S+)", output)
        return match.group(1) if match else None

    def patch(self):
        # The full perl shebang might be too long
        files_to_be_patched_fmt = "bin/{0}.in"
        if self.spec.satisfies("@:1.15.1"):
            files_to_be_patched_fmt = "t/wrap/{0}.in"

        if self.spec.satisfies("@1.16.3:"):
            shebang_string = "^#!@PERL@"
        else:
            shebang_string = "^#!@PERL@ -w"

        for file in ("aclocal", "automake"):
            filter_file(
                shebang_string, "#!/usr/bin/env perl", files_to_be_patched_fmt.format(file)
            )

