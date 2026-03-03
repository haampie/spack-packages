# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys
from pathlib import Path

from spack_repo.builtin.build_systems.generic import Package

from spack.package import *


class Boost(Package):
    """Boost provides free peer-reviewed portable C++ source
    libraries, emphasizing libraries that work well with the C++
    Standard Library.

    Boost libraries are intended to be widely useful, and usable
    across a broad spectrum of applications. The Boost license
    encourages both commercial and non-commercial use.
    """

    homepage = "https://www.boost.org"
    url = "https://downloads.sourceforge.net/project/boost/boost/1.55.0/boost_1_55_0.tar.bz2"
    git = "https://github.com/boostorg/boost.git"
    list_url = "https://sourceforge.net/projects/boost/files/boost/"
    list_depth = 1


    with_default_variants = "boost" + "".join(
        [
            "+atomic",
            "+chrono",
            "+date_time",
            "+exception",
            "+filesystem",
            "+graph",
            "+iostreams",
            "+locale",
            "+log",
            "+math",
            "+program_options",
            "+random",
            "+regex",
            "+serialization",
            "+system",
            "+test",
            "+thread",
            "+timer",
            "+wave",
        ]
    )

    # mpi/python are not installed by default because they pull in many
    # dependencies and/or because there is a great deal of customization
    # possible (and it would be difficult to choose sensible defaults)
    #
    # Boost.Container can be both header-only and compiled. '+container'
    # indicates the compiled version which requires Extended Allocator
    # support. The header-only library is installed when no variant is given.
    all_libs = [
        "atomic",
        "charconv",
        "chrono",
        "cobalt",
        "container",
        "context",
        "contract",
        "conversion",
        "coroutine",
        "date_time",
        "exception",
        "fiber",
        "filesystem",
        "graph",
        "graph_parallel",
        "iostreams",
        "json",
        "locale",
        "log",
        "math",
        "mpi",
        "mqtt5",
        "nowide",
        "program_options",
        "python",
        "random",
        "regex",
        "serialization",
        "signals",
        "signals2",
        "stacktrace",
        "system",
        "test",
        "thread",
        "timer",
        "type_erasure",
        "url",
        "wave",
    ]

    # Add any extra requirements for specific libraries
    # signals library was removed from boost in 1.69
    # https://www.boost.org/releases/1.69.0/#:~:text=Discontinued
    all_libs_opts = {
        "conversion": {"when": "@1.87.0:"},
        "charconv": {"when": "@1.85.0:"},
        "cobalt": {"when": "@1.84.0:"},
        "signals": {"when": "@:1.68"},
        "signals2": {"when": "@1.4:"},
    }

    for lib in all_libs:
        lib_opts = all_libs_opts.get(lib, {})
        variant(lib, default=False, description="Compile with {0} library".format(lib), **lib_opts)

    variant(
        "context-impl",
        default="fcontext",
        values=("fcontext", "ucontext", "winfib"),
        multi=False,
        description="Use the specified backend for boost-context",
        when="@1.65.0: +context",
    )

    variant(
        "cxxstd",
        default="11",
        values=(
            "98",
            "11",
            "14",
            # C++17 is not supported by Boost < 1.63.0.
            conditional("17", when="@1.63.0:"),
            # C++20/2a is not supported by Boost < 1.73.0
            conditional("2a", when="@1.73.0:"),
            conditional("20", when="@1.77.0:"),
            conditional("23", when="@1.79.0:"),
            conditional("26", when="@1.79.0:"),
        ),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    # 1.84.0 dropped support for 98/03
    variant("debug", default=False, description="Switch to the debug version of Boost")
    variant("shared", default=True, description="Additionally build shared libraries")
    variant(
        "multithreaded", default=True, description="Build multi-threaded versions of libraries"
    )
    variant(
        "singlethreaded", default=False, description="Build single-threaded versions of libraries"
    )
    variant("icu", default=False, description="Build with Unicode and ICU suport")
    variant("taggedlayout", default=False, description="Augment library names with build options")
    variant(
        "versionedlayout",
        default=False,
        description="Augment library layout with versioned subdirs",
    )
    variant(
        "clanglibcpp", default=False, description="Compile with clang libc++ instead of libstdc++"
    )
    variant("numpy", default=False, description="Build the Boost NumPy library (requires +python)")
    variant(
        "pic",
        default=False,
        description="Generate position-independent code (PIC), useful "
        "for building static libraries",
    )

    # https://boostorg.github.io/build/manual/develop/index.html#bbv2.builtin.features.visibility
    variant(
        "visibility",
        values=("global", "protected", "hidden"),
        default="hidden",
        multi=False,
        description="Default symbol visibility in compiled libraries (1.69.0 or later)",
    )

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    # https://github.com/boostorg/python/issues/431

    # Improve the error message when the context-impl variant is conflicting
    # boost-mpi depends on boost-python since 1.87.0

    # (https://github.com/spack/spack/pull/32879#issuecomment-1265933265)
    # Boost did not support the oneapi compilers prior to 1.76
    # Boost 1.85.0 stacktrace added a hard compilation error that has to
    # explicitly be suppressed on some platforms:
    # https://github.com/boostorg/stacktrace/pull/150. This conflict could be
    # turned into a variant that allows users to opt-in when they know it is
    # safe to do so on affected platforms.

    # https://github.com/boostorg/python/issues/400

    # On Windows, the signals variant is required when building any of
    # the all_libs variants.
    for lib in all_libs:
        if lib not in ["signals", "signals2"]:
            # <= 1.68 needs signals, after that needs signals2
            requires("+signals", when=f"@:1.68 +{lib} platform=windows")
            requires("+signals2", when=f"@1.69: +{lib} platform=windows")

    # Patch fix from https://svn.boost.org/trac/boost/ticket/11856

    # Patch fix from https://svn.boost.org/trac/boost/ticket/11120

    # Patch fix for IBM XL compiler

    # Patch fix from https://svn.boost.org/trac/boost/ticket/10125

    # Patch to override the PGI toolset when using the NVIDIA compilers

    # Patch to workaround compiler bug

    # Patch to workaround gcc-8.3 compiler issue https://github.com/boostorg/mpl/issues/44

    # Fix for version comparison on newer Clang on darwin
    # See: https://github.com/boostorg/build/issues/440
    # See: https://github.com/macports/macports-ports/pull/6726

    # Fix missing declaration of uintptr_t with glibc>=2.17 - https://bugs.gentoo.org/482372

    # Fix: "Compile issue with flat_tree insert"
    # See: https://github.com/boostorg/container/pull/101

    # Fix: "Unable to compile code using boost/process.hpp"
    # See: https://github.com/boostorg/process/issues/116
    # Patch: https://github.com/boostorg/process/commit/6a4d2ff72114ef47c7afaf92e1042aca3dfa41b0.patch

    # Patch fix for warnings from commits 2d37749, af1dc84, c705bab, and
    # 0134441 on https://github.com/boostorg/system.

    # Change the method for version analysis when using Fujitsu compiler.

    # Add option to C/C++ compile commands in clang-linux.jam

    # C++20 concepts fix for Beast
    # See https://github.com/boostorg/beast/pull/1927 for details

    # Cloning a status_code with indirecting_domain leads to segmentation fault
    # See https://github.com/ned14/outcome/issues/223 for details

    # Support bzip2 and gzip in other directory
    # See https://github.com/boostorg/build/pull/154

    # Backport Python3 import problem
    # See https://github.com/boostorg/python/pull/218

    # Fix B2 bootstrap toolset during installation
    # See https://github.com/spack/spack/issues/20757
    # and https://github.com/spack/spack/pull/21408

    # Fix compiler used for building bjam during bootstrap

    # Allow building context asm sources with GCC on Darwin
    # See https://github.com/spack/spack/pull/24889
    # and https://github.com/boostorg/context/issues/177

    # Fix float128 support when building with CUDA and Cray compiler
    # See https://github.com/boostorg/config/pull/378

    # Fix building with Intel compilers

    # Fix issues with PTHREAD_STACK_MIN not being a DEFINED constant in newer glibc
    # See https://github.com/spack/spack/issues/28273

    # https://www.intel.com/content/www/us/en/developer/articles/technical/building-boost-with-oneapi.html

    # https://github.com/spack/spack/issues/44003

    # https://github.com/boostorg/phoenix/issues/111

    # https://github.com/boostorg/filesystem/issues/284

    # https://github.com/boostorg/context/pull/280

