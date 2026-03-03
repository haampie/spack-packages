# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack_repo.builtin.build_systems.cargo import CargoPackage

from spack.package import *


class Typst(CargoPackage):
    """Typst is a new markup-based typesetting system for the sciences."""

    homepage = "https://typst.app"
    git = "https://github.com/typst/typst"
    executables = ["^typst$"]



    depends_on("rust@1.80:", type="build")
    depends_on("openssl")
    depends_on("pkgconfig", type="build")

    build_directory = "crates/typst-cli"

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"typst ([0-9.]+)", output)
        return match.group(1) if match else None
