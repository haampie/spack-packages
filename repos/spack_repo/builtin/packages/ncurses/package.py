# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.gnu import GNUMirrorPackage

from spack.package import *


class Ncurses(AutotoolsPackage, GNUMirrorPackage):
    """The ncurses (new curses) library is a free software emulation of
    curses in System V Release 4.0, and more. It uses terminfo format,
    supports pads and color and multiple highlights and forms
    characters and function-key mapping, and has all the other
    SYSV-curses enhancements over BSD curses."""

    homepage = "https://invisible-island.net/ncurses/ncurses.html"
    # URL must remain http:// so Spack can bootstrap curl
    gnu_mirror_path = "ncurses/ncurses-6.1.tar.gz"

    executables = [r"^ncursesw?(?:\d+(?:\.\d+)*)?-config$"]

    version(
        "6.5-20250705",
        sha256="73f6c22db6c3fcac562e7b35aebf7d4cbb253ea30ba2ee465ab84d7d1b5cefc1",
        url="https://invisible-mirror.net/archives/ncurses/current/ncurses-6.5-20250705.tgz",
    )
    version("6.5", sha256="136d91bc269a9a5785e5f9e980bc76ab57428f604ce3e5a5a90cebc767971cc6")
    version("6.4", sha256="6931283d9ac87c5073f30b6290c4c75f21632bb4fc3603ac8100812bed248159")
    version("6.3", sha256="97fc51ac2b085d4cde31ef4d2c3122c21abc217e9090a43a30fc5ec21684e059")
    version("6.2", sha256="30306e0c76e0f9f1f0de987cf1c82a5c21e1ce6568b9227f7da5b71cbea86c9d")
    version("6.1", sha256="aa057eeeb4a14d470101eff4597d5833dcef5965331be3528c08d99cebaa0d17")
    version("6.0", sha256="f551c24b30ce8bfb6e96d9f59b42fbea30fa3a6123384172f9e7284bcf647260")
    version("5.9", sha256="9046298fb440324c9d4135ecea7879ffed8546dd1b58e59430ea07a4633f563b")

    # Build ncurses with ABI compaitibility.




    # avoid disallowed const_cast from T* to void* and use reinterpret_cast
    # Ref: https://lists.gnu.org/archive/html/bug-ncurses/2014-08/msg00008.html
