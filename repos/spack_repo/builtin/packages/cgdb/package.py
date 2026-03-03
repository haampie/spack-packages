# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Cgdb(AutotoolsPackage):
    """A curses front-end to GDB"""

    maintainers("tuxfan")
    homepage = "https://cgdb.github.io"
    url = "https://cgdb.me/files/cgdb-0.7.1.tar.gz"
    git = "https://github.com/cgdb/cgdb.git"

    license("GPL-2.0-or-later")

    version("master", branch="master", submodules=False, preferred=True)
    version("0.7.1", sha256="bb723be58ec68cb59a598b8e24a31d10ef31e0e9c277a4de07b2f457fe7de198")
    version("0.7.0", sha256="bf7a9264668db3f9342591b08b2cc3bbb08e235ba2372877b4650b70c6fb5423")


    # Required dependency

    @when("@master")
    def autoreconf(self, spec, prefix):
        sh = which("sh")
        sh("autogen.sh")

    def configure_args(self):
        spec = self.spec

        return [
            "--with-ncurses={0}".format(spec["ncurses"].prefix),
            "--with-readline={0}".format(spec["readline"].prefix),
        ]
