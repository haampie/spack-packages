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

    variant(
        "termlib",
        default=True,
        description="Enables termlib features. This is an extra "
        "lib and optional internal dependency.",
    )
    # Build ncurses with ABI compaitibility.
    variant(
        "abi",
        default="none",
        description="choose abi compatibility",
        values=("none", "5", "6"),
        multi=False,
    )

    conflicts("abi=6", when="@:5.9", msg="6 is not compatible with this release")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated


    # avoid disallowed const_cast from T* to void* and use reinterpret_cast
    # Ref: https://lists.gnu.org/archive/html/bug-ncurses/2014-08/msg00008.html
    patch("rxvt_unicode_6_4.patch", when="@6.1:")

