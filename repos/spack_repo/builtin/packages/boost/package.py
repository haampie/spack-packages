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
    # https://boostorg.github.io/build/manual/develop/index.html#bbv2.builtin.features.visibility
    # Unicode support
    depends_on("icu4c cxxstd=11", when="+icu cxxstd=11")
    # NOTE: 1.64.0 seems fine for *most* applications, but if you need
    #       +python and +mpi, there seem to be errors with out-of-date
    #       API calls from mpi/python.
    #       See: https://github.com/spack/spack/issues/3963
    # boost-python in 1.72.0 broken with cxxstd=98
    # boost-mpi depends on boost-python since 1.87.0
    # Boost.System till 1.76 (included) was relying on mutex, which was not
    # detected correctly on Darwin platform when using GCC
    # https://github.com/spack/spack/issues/44003
    # https://github.com/boostorg/filesystem/issues/284
    # https://github.com/boostorg/context/pull/280
