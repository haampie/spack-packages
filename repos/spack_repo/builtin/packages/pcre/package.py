# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems import autotools, cmake
from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Pcre(AutotoolsPackage, CMakePackage):
    """The PCRE package contains Perl Compatible Regular Expression
    libraries. These are useful for implementing regular expression
    pattern matching using the same syntax and semantics as Perl 5."""

    homepage = "https://www.pcre.org"
    url = "https://sourceforge.net/projects/pcre/files/pcre/8.42/pcre-8.42.tar.bz2"



    build_system("autotools", "cmake", default="autotools")

    variant("jit", default=False, description="Enable JIT support.")

    variant("multibyte", default=True, description="Enable support for 16 and 32 bit characters.")

    variant(
        "utf",
        default=True,
        description="Enable support for UTF-8/16/32, incompatible with EBCDIC.",
    )

    variant("shared", default=True, description="Build shared libraries")
    variant("static", default=True, description="Build static libraries")
    conflicts("-shared -static", msg="Must build one of shared and static")
    conflicts(
        "+shared +static",
        when="build_system=cmake",
        msg="CMake can only build either shared or static",
    )

    variant("pic", default=True, description="Enable position-independent code (PIC)")
    requires("+pic", when="+shared build_system=autotools")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    with when("build_system=cmake"):
        depends_on("zlib")
        depends_on("bzip2")


class AutotoolsBuilder(autotools.AutotoolsBuilder):
    def configure_args(self):
        args = []

        args.extend(self.enable_or_disable("shared"))
        args.extend(self.enable_or_disable("static"))
        args.extend(self.with_or_without("pic"))

        args.extend(self.enable_or_disable("jit"))

        args.extend(self.enable_or_disable("pcre16", variant="multibyte"))
        args.extend(self.enable_or_disable("pcre32", variant="multibyte"))

        args.extend(self.enable_or_disable("utf"))
        args.extend(self.enable_or_disable("unicode-properties", variant="utf"))

        return args


class CMakeBuilder(cmake.CMakeBuilder):
    def cmake_args(self):
        args = []

        args.append(self.define_from_variant("BUILD_SHARED_LIBS", "shared"))
        args.append(self.define_from_variant("BUILD_STATIC_LIBS", "static"))
        args.append(self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"))

        args.append(self.define_from_variant("PCRE_SUPPORT_JIT", "jit"))

        args.append(self.define_from_variant("PCRE_BUILD_PCRE16", "multibyte"))
        args.append(self.define_from_variant("PCRE_BUILD_PCRE32", "multibyte"))

        args.append(self.define_from_variant("PCRE_SUPPORT_UTF", "utf"))
        args.append(self.define_from_variant("PCRE_SUPPORT_UNICODE_PROPERTIES", "utf"))

        return args
