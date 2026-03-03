# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import glob
import os
import sys
from spack_repo.builtin.build_systems import compiler
from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.compiler import CompilerPackage
from spack_repo.builtin.build_systems.gnu import GNUMirrorPackage
from spack.package import *
class Gcc(AutotoolsPackage, GNUMirrorPackage, CompilerPackage):
    """The GNU Compiler Collection includes front ends for C, C++, Objective-C,
    Fortran, Ada, and Go, as well as libraries for these languages."""
    homepage = "https://gcc.gnu.org"
    gnu_mirror_path = "gcc/gcc-9.2.0/gcc-9.2.0.tar.xz"
    git = "git://gcc.gnu.org/git/gcc.git"
    list_url = "https://ftp.gnu.org/gnu/gcc/"
    list_depth = 1
    keep_werror = "all"
    provides("c", "cxx", when="languages=c,c++")
    provides("c", when="languages=c")
    version("master", branch="master")
    # Latest stable
    version("15.2.0", sha256="438fd996826b0c82485a29da03a72d71d6e3541a83ec702df4271f6fe025d24e")
    # Previous stable series releases
    # Final releases of previous versions
    # Deprecated older non-final releases
    with default_args(deprecated=True):
        version("4.8.4", sha256="4a80aa23798b8e9b5793494b8c976b39b8d9aa2e53cd5ed5534aff662a7f8695")
    # In that respect, the name 'all' is rather misleading.
    # (ii) Languages other than c,c++,fortran are prone to configure bug in GCC
    # For example, 'java' appears to ignore custom location of zlib
    # (iii) meaning of 'all' changes with GCC version, i.e. 'java' is not part
    # of gcc7. Correctly specifying conflicts() and depends_on() in such a
    # case is a PITA.
    #
    # Also note that some languages get enabled by the configure scripts even if not listed in the
    # arguments. For example, c++ is enabled when the bootstrapping is enabled and lto is enabled
    # when the link time optimization support is enabled.
    variant(
        "languages",
        default="c,c++,fortran",
        values=(
            "ada",
            "brig",
            "c",
            "c++",
            "d",
            "fortran",
            "go",
            "java",
            "jit",
            "lto",
            "objc",
            "obj-c++",
        ),
        multi=True,
        description="Compilers and runtime libraries to build",
    )
    variant("binutils", default=True, description="Use binutils linker and assembler")
    variant("mold", default=False, description="Use mold as the linker by default", when="@12:")
    variant(
        "piclibs", default=False, description="Build PIC versions of libgfortran.a and libstdc++.a"
    )
    variant("strip", default=False, description="Strip executables to reduce installation size")
    variant("nvptx", default=False, description="Target nvptx offloading to NVIDIA GPUs")
    variant("bootstrap", default=True, description="Enable 3-stage bootstrap")
    variant(
        "graphite", default=False, description="Enable Graphite loop optimizations (requires ISL)"
    )
    variant(
        "build_type",
        default="RelWithDebInfo",
        values=("Debug", "Release", "RelWithDebInfo", "MinSizeRel"),
        description="CMake-like build type. "
        "Debug: -O0 -g; Release: -O3; "
        "RelWithDebInfo: -O2 -g; MinSizeRel: -Os",
    )
    variant(
        "profiled", default=False, description="Use Profile Guided Optimization", when="+bootstrap"
    )
    # https://gcc.gnu.org/install/prerequisites.html
    # mawk is not sufficient for go support
    # dependencies required for git versions
    # GCC 7.3 does not compile with newer releases on some platforms, see
    #   https://github.com/spack/spack/issues/6902#issuecomment-433030376
    # Already released GCC versions do not support any newer version of ISL
    #   GCC 5.4 https://github.com/spack/spack/issues/6902#issuecomment-433072097
    #   GCC 7.3 https://github.com/spack/spack/issues/6902#issuecomment-433030376
    #   GCC 9+  https://gcc.gnu.org/bugzilla/show_bug.cgi?id=86724
    with when("+graphite"):
        depends_on("isl@0.14", when="@5.0:5.2")
    # The server is sometimes a bit slow to respond
    timeout = {"timeout": 60}
    # TODO: integrate these libraries.
    # depends_on('ppl')
    # depends_on('cloog')
    # https://gcc.gnu.org/install/test.html
    # See https://go.dev/doc/install/gccgo#Releases
    with when("languages=go"):
        provides("go-or-gccgo-bootstrap@:1.0", when="@4.7.1:")
    # For a list of valid languages for a specific release,
    # BRIG does not seem to be supported on macOS
    # GCC 4.8 added a 'c' language. I'm sure C was always built,
    # but this is the first version that accepts 'c' as a valid language.
    # The GCC Java frontend and associated libjava runtime library
    # have been removed from GCC as of GCC 7.
    # See https://gcc.gnu.org/gcc-7/changes.html
    # GCC 5 added the ability to build GCC as a Just-In-Time compiler.
    # See https://gcc.gnu.org/gcc-5/changes.html
    with when("languages=d"):
        # Support for the D programming language has been added to GCC 9.
        # See https://gcc.gnu.org/gcc-9/changes.html#d
        conflicts("@:8", msg="support for D has been added in GCC 9.1")
        # See https://gcc.gnu.org/install/prerequisites.html#GDC-prerequisite
        with when("@12:"):
            # All versions starting 12 have to be built GCC:
            # And it has to be GCC older than the version we build:
            vv = ["11", "12.1.0", "12.2.0"]
            for prev_v, curr_v in zip(vv, vv[1:]):
                conflicts(
                    "%gcc@{0}:".format(curr_v),
                    when="@{0}".format(curr_v),
                    msg="'gcc@{0} languages=d' requires '%gcc@:{1}' "
                    "with the D language support".format(curr_v, prev_v),
                )
            # See https://github.com/D-Programming-GDC/gdc
            # We, however, require at least the oldest version that officially supports GDC. It is
            # also a good opportunity to tell the users that they need a working GDC:
    # GPU offload backend supported by limited languages
    with when("+nvptx"):
        conflicts("languages=d")
    # Newlib version table
    newlib_shasum = {
        "3.0.0.20180831": "3ad3664f227357df15ff34e954bfd9f501009a647667cd307bf0658aefd6eb5b",
        "3.3.0": "58dd9e3eaedf519360d92d84205c3deef0b3fc286685d1c562e245914ef72c66",
        "4.1.0": "f296e372f51324224d387cc116dc37a6bd397198756746f93a2b02e9a5d40154",
        "4.2.0.20211231": "c3a0e8b63bc3bef1aeee4ca3906b53b3b86c8d139867607369cb2915ffc54435",
        "4.3.0.20230120": "83a62a99af59e38eb9b0c58ed092ee24d700fff43a22c03e433955113ef35150",
        "4.4.0.20231231": "0c166a39e1bf0951dfafcd68949fe0e4b6d3658081d6282f39aeefc6310f2f13",
        "4.5.0.20241231": "33f12605e0054965996c25c1382b3e463b0af91799001f5bb8c0630f2ec8c852",
    }
    with when("+nvptx"):
        nvptx_newlib_ver = "4.5.0.20241231"
        resource(
            name="newlib",
            url="ftp://sourceware.org/pub/newlib/newlib-{0}.tar.gz".format(nvptx_newlib_ver),
            sha256=newlib_shasum[nvptx_newlib_ver],
            destination="newlibsource",
            fetch_options=timeout,
        )
        nvptx_tools_ver = "2023-09-13"
        # NVPTX offloading supported in 7 and later by limited languages
        # NVPTX build disables bootstrap
    # Bootstrap comparison failure:
    #   see https://github.com/spack/spack/issues/23296
    #   https://gcc.gnu.org/bugzilla/show_bug.cgi?id=100340
    #   on XCode 12.5
    # GCC 11 requires GCC 4.8 or later (https://gcc.gnu.org/gcc-11/changes.html)
    # https://github.com/iains/gcc-12-branch/issues/6
    # Applies
    # https://github.com/gcc-mirror/gcc/commit/ea2798892de373b14f9fc7ae8a0d820eaddca98c,
    # which fixes an incorrectly applied fixincludes rule for pthread.h, making
    # the installed GCC not portable across different glibc versions. Original
    # GCC bug report: https://gcc.gnu.org/bugzilla/show_bug.cgi?id=118009. For
    # GCC 15 we can directly use the upstream patch. For GCC 12-14 the patch
    # has been backported. The patch is not applied to GCC 11 since the "fixinclude"
    # is in fact needed for that version (see GCC commit description). Older versions
    # have not been checked or tested.
    patch(
        "https://github.com/gcc-mirror/gcc/commit/ea2798892de373b14f9fc7ae8a0d820eaddca98c.patch?full_index=1",
        sha256="0999dbf856725566373f25a6f192a3520ea036db8e1f31928aae9750e6e38be7",
        when="@15:15.2",
    )
    if sys.platform == "darwin":
        # Fix parallel build on APFS filesystem
        # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=81797
        if macos_version() >= Version("10.13"):
            # from homebrew via macports
            # https://trac.macports.org/ticket/56502#no1
            # see also: https://gcc.gnu.org/bugzilla/show_bug.cgi?id=83531
            patch("darwin/headers-10.13-fix.patch", when="@5.5.0")
        if macos_version() >= Version("10.14"):
            # Fix system headers for Mojave SDK:
            # https://github.com/Homebrew/homebrew-core/pull/39041
            patch(
                "https://raw.githubusercontent.com/Homebrew/formula-patches/b8b8e65e/gcc/8.3.0-xcode-bug-_Atomic-fix.patch",
                sha256="33ee92bf678586357ee8ab9d2faddf807e671ad37b97afdd102d5d153d03ca84",
                when="@6:8.3",
            )
            # See https://raw.githubusercontent.com/Homebrew/homebrew-core/3b7db4457ac64a31e3bbffc54b04c4bd824a4a4a/Formula/gcc.rb
