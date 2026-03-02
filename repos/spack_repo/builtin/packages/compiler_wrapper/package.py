# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pathlib
import shutil
import sys
from spack_repo.builtin.build_systems.generic import Package
from spack.package import *
class CompilerWrapper(Package):
    """Spack compiler wrapper script.
    Compiler commands go through this compiler wrapper in Spack builds.
    The compiler wrapper is a thin layer around the standard compilers.
    """
    homepage = "https://github.com/spack/spack"
    url = f"file:///{pathlib.PurePath(__file__).parent}/cc.sh"
    # FIXME (compiler as nodes): use a different tag, since this is only to exclude
    # this node from auto-generated rules
    tags = ["runtime"]
    if sys.platform != "win32":
        version(
            "1.0",
            sha256="c7b816479554fd32f677db15ceec6627b91c86074a5d65498688afcbe2796188",
            expand=False,
        )
