# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class Figlet(MakefilePackage):
    """FIGlet is a program that creates large characters out of ordinary
    screen characters."""

    homepage = "http://www.figlet.org/"
    url = "https://github.com/cmatsuoka/figlet/archive/2.2.5.tar.gz"



    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        bins = ["figlet", "chkfont", "figlist", "showfigfonts"]
        for f in bins:
            install(f, prefix.bin)

        mkdirp(prefix.man6)
        manuals = ["figlet.6", "chkfont.6", "figlist.6", "showfigfonts.6"]
        for f in manuals:
            install(f, prefix.man6)

        install_tree("./fonts", prefix.share.figlet)

    @property
    def build_targets(self):
        return ["DEFAULTFONTDIR=" + self.prefix.share.figlet]
