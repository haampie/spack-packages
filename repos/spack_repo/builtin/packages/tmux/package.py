# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Tmux(AutotoolsPackage):
    """Tmux is a terminal multiplexer.

    What is a terminal multiplexer? It lets you switch easily between several
    programs in one terminal, detach them (they keep running in the
    background) and reattach them to a different terminal. And do a lot more.
    """

    homepage = "https://tmux.github.io"
    url = "https://github.com/tmux/tmux/releases/download/2.6/tmux-2.6.tar.gz"
    git = "https://github.com/tmux/tmux.git"


    variant(
        "utf8proc", default=False, description="Build with UTF-8 support from utf8proc library"
    )
    variant("static", default=False, description="Create a static build")
    variant(
        "jemalloc", default=False, description="Use jemalloc for memory allocation", when="@3.5:"
    )

    depends_on("c", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("automake", type="build", when="@master")
    depends_on("autoconf", type="build", when="@master")
    depends_on("yacc", type="build", when="@3:")
    depends_on("libevent")
    depends_on("ncurses")
    depends_on("utf8proc", when="+utf8proc")
    depends_on("jemalloc", when="+jemalloc")

    conflicts("+static", when="platform=darwin", msg="Static build not supported on MacOS")

    patch(
        "https://github.com/tmux/tmux/commit/775789fbd5c4f3aa93061480cd64e61daf7fb689.patch?full_index=1",
        sha256="c1b61a1244f758480578888d3f89cac470271c376ea0879996b81e10b397cad0",
        when="@2.4:3.4",
    )

    @run_before("autoreconf")
    def autogen(self):
        if self.spec.satisfies("@master"):
            sh = which("sh")
            sh("autogen.sh")

    def configure_args(self):
        args = []
        args.extend(self.enable_or_disable("utf8proc"))
        args.extend(self.enable_or_disable("static"))
        args.extend(self.enable_or_disable("jemalloc"))
        return args
