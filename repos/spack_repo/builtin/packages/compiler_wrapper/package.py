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
    It enables several key pieces of functionality:

    1. It allows Spack to swap compilers into and out of builds easily.
    2. It adds several options to the compile line so that spack
       packages can find their dependencies at build time and run time:
       -I and/or -isystem arguments for dependency /include directories.
       -L                 arguments for dependency /lib directories.
       -Wl,-rpath         arguments for dependency /lib directories.
    3. It provides a mechanism to inject flags from specs
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
    else:
        version("1.0")
        has_code = False

