# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Uchardet(CMakePackage):
    """uchardet is an encoding detector library, which takes a sequence of
    bytes in an unknown character encoding without any additional information,
    and attempts to determine the encoding of the text. Returned encoding names
    are iconv-compatible."""

    homepage = "https://www.freedesktop.org/wiki/Software/uchardet/"
    url = "https://www.freedesktop.org/software/uchardet/releases/uchardet-0.0.6.tar.xz"
    git = "https://gitlab.freedesktop.org/uchardet/uchardet.git"



    def url_for_version(self, version):
        if version >= Version("0.0.6"):
            url = "https://www.freedesktop.org/software/uchardet/releases/uchardet-0.0.6.tar.xz"
        else:
            url = "https://github.com/BYVoid/uchardet/archive/v0.0.5.tar.gz"
        return url

    def cmake_args(self):
        args = []
        if self.spec.satisfies("platform=darwin"):
            args += [
                # From https://github.com/Homebrew/homebrew-core/blob/HEAD/Formula/uchardet.rb
                self.define("CMAKE_INSTALL_NAME_DIR", self.prefix.lib),
                # From https://github.com/mutationpp/Mutationpp/issues/26
                self.define("CMAKE_MACOSX_RPATH", "ON"),
            ]
        return args
