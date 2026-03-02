# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack_repo.builtin.build_systems.cmake import CMakeBuilder, CMakePackage
from spack_repo.builtin.build_systems.makefile import MakefileBuilder, MakefilePackage

from spack.package import *


class Zstd(CMakePackage, MakefilePackage):
    """Zstandard, or zstd as short version, is a fast lossless compression
    algorithm, targeting real-time compression scenarios at zlib-level and
    better compression ratios."""

    homepage = "https://facebook.github.io/zstd/"
    url = "https://github.com/facebook/zstd/archive/v1.4.3.tar.gz"
    git = "https://github.com/facebook/zstd.git"







    # +programs builds vendored xxhash, which uses unsupported builtins
    # (last tested: nvhpc@22.3)


    build_system("cmake", "makefile", default="makefile")


class CMakeBuilder(CMakeBuilder):
    @property
    def root_cmakelists_dir(self):
        return os.path.join(super().root_cmakelists_dir, "build", "cmake")

    def cmake_args(self):
        spec = self.spec
        args = []
        args.append(self.define_from_variant("ZSTD_BUILD_PROGRAMS", "programs"))
        args.extend(
            [
                self.define("ZSTD_BUILD_STATIC", self.spec.satisfies("libs=static")),
                self.define("ZSTD_BUILD_SHARED", self.spec.satisfies("libs=shared")),
            ]
        )
        if "compression=zlib" in spec:
            args.append(self.define("ZSTD_ZLIB_SUPPORT", True))
        if "compression=lzma" in spec:
            args.append(self.define("ZSTD_LZMA_SUPPORT", True))
        if "compression=lz4" in spec:
            args.append(self.define("ZSTD_LZ4_SUPPORT", True))
        return args


class MakefileBuilder(MakefileBuilder):
    def build(self, pkg, spec, prefix):
        pass

    def install(self, pkg, spec, prefix):
        args = ["VERBOSE=1", "PREFIX=" + prefix]

        # Tested %nvhpc@22.3. No support for -MP
        if "%nvhpc" in self.spec:
            args.append("DEPFLAGS=-MT $@ -MMD -MF")
        # library targets
        lib_args = ["-C", "lib"] + args + ["install-pc", "install-includes"]
        if "libs=shared" in spec:
            lib_args.append("install-shared")
        if "libs=static" in spec:
            lib_args.append("install-static")

        # install the library
        make(*lib_args)
        # install the programs
        if "+programs" in spec:
            programs_args = ["-C", "programs"] + args
            # additional compression programs have to be turned off, otherwise the
            # makefile will detect them.
            if "compression=zlib" not in spec:
                programs_args.append("HAVE_ZLIB=0")
            if "compression=lzma" not in spec:
                programs_args.append("HAVE_LZMA=0")
            if "compression=lz4" not in spec:
                programs_args.append("HAVE_LZ4=0")
            programs_args.append("install")
            make(*programs_args)
