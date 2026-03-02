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



    version("1.5.7", sha256="37d7284556b20954e56e1ca85b80226768902e2edabd3b649e9e72c0c9012ee3")
    version("1.5.6", sha256="30f35f71c1203369dc979ecde0400ffea93c27391bfd2ac5a9715d2173d92ff7")
    version("1.5.5", sha256="98e9c3d949d1b924e28e01eccb7deed865eefebf25c2f21c702e5cd5b63b85e1")
    version("1.4.8", sha256="f176f0626cb797022fbf257c3c644d71c1c747bb74c32201f9203654da35e9fa")
    version("1.4.7", sha256="085500c8d0b9c83afbc1dc0d8b4889336ad019eba930c5d6a9c6c86c20c769c8")
    version("1.3.8", sha256="90d902a1282cc4e197a8023b6d6e8d331c1fd1dfe60f7f8e4ee9da40da886dc3")




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
