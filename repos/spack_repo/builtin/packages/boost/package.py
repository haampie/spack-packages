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

    @property
    def libs(self):
        query = self.spec.last_query.extra_parameters
        shared = "+shared" in self.spec

        libnames = (
            query if query else [lib for lib in self.all_libs if self.spec.satisfies("+%s" % lib)]
        )
        libnames += ["monitor"]
        libraries = ["libboost_*%s*" % lib for lib in libnames]

        return find_libraries(libraries, root=self.prefix, shared=shared, recursive=True)

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
    conflicts("cxxstd=98", when="@1.84.0:")

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


    # Unicode support
    depends_on("icu4c cxxstd=11", when="+icu cxxstd=11")
    # NOTE: 1.64.0 seems fine for *most* applications, but if you need
    #       +python and +mpi, there seem to be errors with out-of-date
    #       API calls from mpi/python.
    #       See: https://github.com/spack/spack/issues/3963
    conflicts("+numpy", when="~python")

    # boost-python in 1.72.0 broken with cxxstd=98
    conflicts("cxxstd=98", when="+mpi+python @1.72.0")

    # boost-mpi depends on boost-python since 1.87.0
    conflicts("~python", when="+mpi @1.87.0:")

    # Container's Extended Allocators were not added until 1.56.0
    conflicts("+container", when="@:1.55")

    # Boost.System till 1.76 (included) was relying on mutex, which was not
    # detected correctly on Darwin platform when using GCC
    #
    # More details here:
    # https://github.com/STEllAR-GROUP/hpx/issues/5442#issuecomment-878889166
    # https://github.com/STEllAR-GROUP/hpx/issues/5442#issuecomment-878913339

    # Boost 1.80 does not build with the Intel oneapi compiler
    # (https://github.com/spack/spack/pull/32879#issuecomment-1265933265)

    # Boost did not support the oneapi compilers prior to 1.76

    # Boost 1.85.0 stacktrace added a hard compilation error that has to
    # explicitly be suppressed on some platforms:
    # https://github.com/boostorg/stacktrace/pull/150. This conflict could be
    # turned into a variant that allows users to opt-in when they know it is
    # safe to do so on affected platforms.

    # https://github.com/boostorg/python/issues/400
    conflicts(
        "@:1.80.0",
        when="+python ^python@3.11:",
        msg="Boost.python.enum has a known bug for boost@:1.80.0 and python@3.11:",
    )

    # On Windows, the signals variant is required when building any of
    # the all_libs variants.
    for lib in all_libs:
        if lib not in ["signals", "signals2"]:
            # <= 1.68 needs signals, after that needs signals2
            requires("+signals", when=f"@:1.68 +{lib} platform=windows")
            requires("+signals2", when=f"@1.69: +{lib} platform=windows")

    # Patch fix from https://svn.boost.org/trac/boost/ticket/11120

    # Patch fix for IBM XL compiler

    # Patch fix from https://svn.boost.org/trac/boost/ticket/10125
    # Patch to override the PGI toolset when using the NVIDIA compilers

    # Fix for version comparison on newer Clang on darwin
    # See: https://github.com/macports/macports-ports/pull/6726
    # Fix: "Compile issue with flat_tree insert"

    # Fix: "Unable to compile code using boost/process.hpp"
    # Change the method for version analysis when using Fujitsu compiler.

    # Add option to C/C++ compile commands in clang-linux.jam
    # See https://github.com/ned14/outcome/issues/223 for details

    # Support bzip2 and gzip in other directory
    # See https://github.com/boostorg/build/pull/154

    # Backport Python3 import problem
    # See https://github.com/boostorg/python/pull/218

    # Fix B2 bootstrap toolset during installation
    # and https://github.com/spack/spack/pull/21408


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


    # https://github.com/boostorg/filesystem/issues/284
    # https://github.com/boostorg/context/pull/280

    def patch(self):
        # Disable SSSE3 and AVX2 when using the NVIDIA compiler
            filter_file("dump_avx2", "", "libs/log/build/Jamfile.v2")
