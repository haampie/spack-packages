# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Mc(AutotoolsPackage):
    """The GNU Midnight Commander is a visual file manager."""

    homepage = "https://midnight-commander.org"
    url = "http://ftp.midnight-commander.org/mc-4.8.20.tar.bz2"

    license("GPL-3.0-or-later")

    version("4.8.31", sha256="f42f4114ed42f6cf9995f1d896fa6c797ccb36dac57760dda8dd9f78ac462841")
    version("4.8.28", sha256="6bb47533d7a55bb21e46292d2f94786c9037bd7a70bf02b6a3c48adb0c9ce20c")

    depends_on("c", type="build")  # generated

    depends_on("ncurses")
    depends_on("pkgconfig", type="build")
    depends_on("glib@2.14:")
    depends_on("libssh2@1.2.5:")

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        # Fix compilation bug on macOS by pretending we don't have utimensat()
        # https://github.com/MidnightCommander/mc/pull/130
        if "darwin" in self.spec.architecture:
            env.set("ac_cv_func_utimensat", "no")

    def configure_args(self):
        args = [
            f"CFLAGS={self.compiler.c99_flag}",
            "--disable-debug",
            "--disable-dependency-tracking",
            "--disable-silent-rules",
            "--without-x",
            "--with-screen=ncurses",
            "--enable-vfs-sftp",
        ]
        return args
