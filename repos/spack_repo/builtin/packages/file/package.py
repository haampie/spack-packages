# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class File(AutotoolsPackage):
    """The file command is "a file type guesser", that is, a command-line
    tool that tells you in words what kind of data a file contains"""

    homepage = "https://www.darwinsys.com/file/"
    url = "https://astron.com/pub/file/file-5.37.tar.gz"



    executables = ["^file$"]

    variant("static", default=True, description="Also build static libraries")



    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"file-(\S+)", output)
        return match.group(1) if match else None

    def configure_args(self):
        args = [
            "--disable-dependency-tracking",
            "--enable-fsect-man5",
            "--enable-zlib",
            "--enable-bzlib",
            "--enable-xzlib",
            "--enable-zstdlib",
            "--disable-lzlib",
        ]
        args += self.enable_or_disable("static")
        return args
