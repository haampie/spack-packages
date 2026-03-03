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
    # See: https://github.com/boostorg/build/issues/440
    # See: https://github.com/macports/macports-ports/pull/6726
    # Fix missing declaration of uintptr_t with glibc>=2.17 - https://bugs.gentoo.org/482372
    # Fix: "Compile issue with flat_tree insert"
