# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.gnu import GNUMirrorPackage

from spack.package import *


class Gdbm(AutotoolsPackage, GNUMirrorPackage):
    """GNU dbm (or GDBM, for short) is a library of database functions
    that use extensible hashing and work similar to the standard UNIX dbm.
    These routines are provided to a programmer needing to create and
    manipulate a hashed database."""

    homepage = "https://www.gnu.org.ua/software/gdbm/gdbm.html"
    gnu_mirror_path = "gdbm/gdbm-1.13.tar.gz"

    license("GPL-3.0-or-later")

    version("1.26", sha256="6a24504a14de4a744103dcb936be976df6fbe88ccff26065e54c1c47946f4a5e")
    version("1.25", sha256="d02db3c5926ed877f8817b81cd1f92f53ef74ca8c6db543fbba0271b34f393ec")
    version("1.24", sha256="695e9827fdf763513f133910bc7e6cfdb9187943a4fec943e57449723d2b8dbf")
    version("1.23", sha256="74b1081d21fff13ae4bd7c16e5d6e504a4c26f7cde1dca0d963a484174bbcacd")
    version("1.18.1", sha256="86e613527e5dba544e73208f42b78b7c022d4fa5a6d5498bf18c8d6f745b91dc")
    version("1.14.1", sha256="cdceff00ffe014495bed3aed71c7910aa88bf29379f795abc0f46d4ee5f8bc5f")
    version("1.13", sha256="9d252cbd7d793f7b12bcceaddda98d257c14f4d1890d851c386c37207000a253")
    version("1.12", sha256="d97b2166ee867fd6ca5c022efee80702d6f30dd66af0e03ed092285c3af9bcea")



    # Fix nanosleep build error: https://cgit.git.savannah.gnu.org/cgit/gdbm.git/commit/?id=ed0a865345681982ea02c6159c0f3d7702c928a1

    patch("gdbm.patch", when="@:1.18 %gcc@10:")
    patch("gdbm.patch", when="@:1.18 %clang@11:")
    patch("gdbm.patch", when="@:1.18 %cce@11:")
    patch("gdbm.patch", when="@:1.18 %aocc@2:")

    def flag_handler(self, name, flags):
        if name == "cflags":
            # See https://src.fedoraproject.org/rpms/gdbm/blob/44ea7380c69b1c139fe385bc1c5940070b36c626/f/gdbm.spec#_62
            if self.spec.satisfies("@:1.24 %gcc@15:"):
                flags.append("-std=gnu11")

        return (flags, None, None)

    def configure_args(self):
        # GDBM uses some non-standard GNU extensions,
        # enabled with -D_GNU_SOURCE.  See:
        #   https://patchwork.ozlabs.org/patch/771300/
        #   https://stackoverflow.com/questions/5582211
        #   https://www.gnu.org/software/automake/manual/html_node/Flag-Variables-Ordering.html
        return ["--enable-libgdbm-compat", "CPPFLAGS=-D_GNU_SOURCE"]
