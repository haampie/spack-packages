# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os
import re

from spack_repo.builtin.build_systems.autotools import AutotoolsBuilder, AutotoolsPackage
from spack_repo.builtin.build_systems.msbuild import MSBuildBuilder, MSBuildPackage
from spack_repo.builtin.build_systems.sourceforge import SourceforgePackage

from spack.package import *


class Xz(MSBuildPackage, AutotoolsPackage, SourceforgePackage):
    """XZ Utils is free general-purpose data compression software with
    high compression ratio. XZ Utils were written for POSIX-like systems,
    but also work on some not-so-POSIX systems. XZ Utils are the successor
    to LZMA Utils."""

    homepage = "https://tukaani.org/xz/"
    sourceforge_mirror_path = "lzmautils/files/xz-5.2.5.tar.bz2"
    list_url = "https://tukaani.org/xz/old.html"


    executables = [r"^xz$"]

    version("5.6.3", sha256="a95a49147b2dbb5487517acc0adcd77f9c2032cf00664eeae352405357d14a6c")
    # ALERT: don't add XZ 5.6.0 or 5.6.1, https://nvd.nist.gov/vuln/detail/CVE-2024-3094

    variant("pic", default=False, description="Compile with position independent code.")

    variant(
        "libs",
        default="shared,static",
        values=("shared", "static"),
        multi=True,
        description="Build shared libs, static libs or both",
    )

    depends_on("c", type="build")  # generated

    # xz-5.2.7/src/liblzma/common/common.h:56 uses attribute __symver__ instead of
    # __asm__(.symver) for newer GCC releases.
    # prior to 5.2.3, build system is for MinGW only, not currently supported by Spack


    build_system(conditional("msbuild", when="platform=windows"), "autotools", default="autotools")

    def flag_handler(self, name, flags):
        if name == "cflags" and "+pic" in self.spec:
            flags.append(self.compiler.cc_pic_flag)
        return (flags, None, None)

    @property
    def libs(self):
        return find_libraries(
            ["liblzma"],
            root=self.prefix,
            recursive=True,
            shared=self.spec.satisfies("libs=shared"),
        )

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"xz \(XZ Utils\) (\S+)", output)
        return match.group(1) if match else None


class AutotoolsBuilder(AutotoolsBuilder):
    def configure_args(self):
        return self.enable_or_disable("libs")

    @run_after("install")
    def darwin_fix(self):
        if self.spec.satisfies("platform=darwin"):
            fix_darwin_install_name(self.prefix.lib)


class MSBuildBuilder(MSBuildBuilder):
    @property
    def build_directory(self):
        def get_file_string_number(f):
            s = re.findall(r"\d+$", f)
            return (int(s[0]) if s else -1, f)

        win_dir = os.path.join(super().build_directory, "windows")
        compiler_dirs = []
        with working_dir(win_dir):
            for obj in os.scandir():
                if obj.is_dir():
                    compiler_dirs.append(obj.name)
        newest_compiler = max(compiler_dirs, key=get_file_string_number)
        return os.path.join(win_dir, newest_compiler)

    def is_64bit(self):
        return "64" in str(self.pkg.spec.target.family)

    def msbuild_args(self):
        plat = "x64" if self.is_64bit() else "x86"
        if self.pkg.spec.satisfies("libs=shared,static"):
            f = "xz_win.sln"
        elif self.pkg.spec.satisfies("libs=shared"):
            f = "liblzma_dll.vcxproj"
        else:
            f = "liblzma.vcxproj"
        return [self.define("Configuration", "Release"), self.define("Platform", plat), f]

    def install(self, pkg, spec, prefix):
        with working_dir(self.build_directory):
            mkdirp(prefix.lib)
            mkdirp(prefix.bin)
            libs_to_find = []
            dlls_to_find = []
            if self.pkg.spec.satisfies("libs=shared"):
                dlls_to_find.append("*.dll")
            if self.pkg.spec.satisfies("libs=static"):
                libs_to_find.append("*.lib")
            for lib in libs_to_find:
                libs_to_install = glob.glob(
                    os.path.join(self.build_directory, "**", lib), recursive=True
                )
                for lib_to_install in libs_to_install:
                    install(lib_to_install, prefix.lib)
            for dll in dlls_to_find:
                dlls_to_install = glob.glob(
                    os.path.join(self.build_directory, "**", dll), recursive=True
                )
                for dll_to_install in dlls_to_install:
                    install(dll_to_install, prefix.bin)

        with working_dir(pkg.stage.source_path):
            install_tree(os.path.join("src", "liblzma", "api"), prefix.include)
