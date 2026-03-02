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


    version("1.88.0", sha256="46d9d2c06637b219270877c9e16155cbd015b6dc84349af064c088e9b5b12f7b")
    version("1.87.0", sha256="af57be25cb4c4f4b413ed692fe378affb4352ea50fbe294a11ef548f4d527d89")
    version("1.86.0", sha256="1bed88e40401b2cb7a1f76d4bab499e352fa4d0c5f31c0dbae64e24d34d7513b")
    version("1.85.0", sha256="7009fe1faa1697476bdc7027703a2badb84e849b7b0baad5086b087b971f8617")
    version("1.84.0", sha256="cc4b893acf645c9d4b698e9a0f08ca8846aa5d6c68275c14c3e7949c24109454")
    version("1.83.0", sha256="6478edfe2f3305127cffe8caf73ea0176c53769f4bf1585be237eb30798c3b8e")
    version("1.82.0", sha256="a6e1ab9b0860e6a2881dd7b21fe9f737a095e5f33a3a874afc6a345228597ee6")
    version("1.81.0", sha256="71feeed900fbccca04a3b4f2f84a7c217186f28a940ed8b7ed4725986baf99fa")
    version("1.80.0", sha256="1e19565d82e43bc59209a168f5ac899d3ba471d55c7610c677d4ccf2c9c500c0")
    version("1.71.0", sha256="d73a8da01e8bf8c7eda40b4c84915071a8c8a0df4a6734537ddde4a8580524ee")
    version("1.70.0", sha256="430ae8354789de4fd19ee52f3b1f739e1fba576f0aded0897c3c2bc00fb38778")
    version("1.48.0", sha256="1bf254b2d69393ccd57a3cdd30a2f80318a005de8883a0792ed2f5e2598e5ada")
    version("1.47.0", sha256="815a5d9faac4dbd523fbcf3fe1065e443c0bbf43427c44aa423422c6ec4c2e31")
    version("1.46.1", sha256="e1dfbf42b16e5015c46b98e9899c423ca4d04469cbeee05e43ea19236416d883")
    version("1.46.0", sha256="2f90f60792fdc25e674b8a857a0bcbb8d01199651719c90d5c4f8c61c08eba59")
    version("1.45.0", sha256="55ed3ec51d5687e8224c988e22bef215dacce04e037d9f689569a80c4377a6d5")
    version("1.40.0", sha256="36cf4a239b587067a4923fdf6e290525a14c3af29829524fa73f3dec6841530c")
    version("1.39.0", sha256="44785eae8c6cce61a29a8a51f9b737e57b34d66baa7c0bcd4af188832b8018fd")

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
    depends_on("icu4c cxxstd=14", when="+icu cxxstd=14")
    depends_on("icu4c cxxstd=17", when="+icu cxxstd=17")

    # https://github.com/boostorg/python/commit/cbd2d9f033c61d29d0a1df14951f4ec91e7d05cd

    # https://github.com/boostorg/python/issues/431

    # Improve the error message when the context-impl variant is conflicting

    # Coroutine, Context, Fiber, etc., are not straightforward.
    conflicts("~context", when="+fiber")  # Fiber requires Context.

    # NOTE: 1.64.0 seems fine for *most* applications, but if you need
    #       +python and +mpi, there seem to be errors with out-of-date
    #       API calls from mpi/python.
    #       See: https://github.com/spack/spack/issues/3963
    conflicts("@1.64.0", when="+python", msg="Errors with out-of-date API calls from Python")
    conflicts("@1.64.0", when="+mpi", msg="Errors with out-of-date API calls from MPI")

    conflicts("+taggedlayout", when="+versionedlayout")
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

    # Patch fix from https://svn.boost.org/trac/boost/ticket/11856
    patch("boost_11856.patch", when="@1.60.0%gcc@4.4.7")

    # Patch fix from https://svn.boost.org/trac/boost/ticket/11120

    # Patch fix for IBM XL compiler
    patch("xl_1_62_0_le.patch", when="@1.62.0%xl")

    # Patch fix from https://svn.boost.org/trac/boost/ticket/10125
    patch("call_once_variadic.patch", when="@1.54.0:1.55%gcc@5.0:")

    # Patch to override the PGI toolset when using the NVIDIA compilers
    patch("nvhpc-1.74.patch", when="@1.74.0:1.75%nvhpc")
    patch("nvhpc-1.76.patch", when="@1.76.0:1.76%nvhpc")

    # Patch to workaround compiler bug
    patch("nvhpc-find_address.patch", when="@1.75.0:1.76%nvhpc")

    patch("boost_gcc83_cpp17_fix.patch", when="@1.69:%gcc@8.3")
    # Fix for version comparison on newer Clang on darwin
    # See: https://github.com/macports/macports-ports/pull/6726
    patch("darwin_clang_version.patch", level=0, when="@1.56.0:1.72.0 platform=darwin")
    patch(
        "https://482372.bugs.gentoo.org/attachment.cgi?id=356970",
        when="@1.53.0:1.54",
        sha256="b6f6ce68282159d46c716a1e6c819c815914bdb096cddc516fa48134209659f2",
    )

    # Fix: "Compile issue with flat_tree insert"
    # See: https://github.com/boostorg/container/pull/101
    patch(
        "container_PR101.patch",
        when="@1.66.0:1.69.0",
        sha256="d216bf7c826c577912aa518c76c17697898483f95336cc035ae9ed16b12dc2b0",
    )

    # Fix: "Unable to compile code using boost/process.hpp"
    # See: https://github.com/boostorg/process/issues/116
    # Patch: https://github.com/boostorg/process/commit/6a4d2ff72114ef47c7afaf92e1042aca3dfa41b0.patch

    # Patch fix for warnings from commits 2d37749, af1dc84, c705bab, and
    # 0134441 on https://github.com/boostorg/system.

    # Change the method for version analysis when using Fujitsu compiler.
    patch("fujitsu_version_analysis-1.77.patch", when="@1.77.0:%fj")

    # Add option to C/C++ compile commands in clang-linux.jam
    patch("clang-linux_add_option.patch", when="@1.56.0:1.63.0")

    # C++20 concepts fix for Beast
    # See https://github.com/boostorg/beast/pull/1927 for details

    # Cloning a status_code with indirecting_domain leads to segmentation fault
    # See https://github.com/ned14/outcome/issues/223 for details

    # Support bzip2 and gzip in other directory
    # See https://github.com/boostorg/build/pull/154

    # Backport Python3 import problem
    # See https://github.com/boostorg/python/pull/218
    patch("boost_218.patch", when="@1.63.0:1.67")

    # Fix B2 bootstrap toolset during installation
    # See https://github.com/spack/spack/issues/20757
    # and https://github.com/spack/spack/pull/21408
    patch("bootstrap-toolset.patch", when="@1.75")

    # Fix compiler used for building bjam during bootstrap
    patch("bootstrap-compiler.patch", when="@1.76:")

    # Allow building context asm sources with GCC on Darwin
    # See https://github.com/spack/spack/pull/24889
    # and https://github.com/boostorg/context/issues/177
    patch("context-macho-gcc.patch", when="@1.65:1.76 +context platform=darwin %gcc")

    # Fix float128 support when building with CUDA and Cray compiler
    # See https://github.com/boostorg/config/pull/378
    patch(
        "https://github.com/boostorg/config/commit/fee1ad07968386b6d547f089311b7a2c1bf7fa55.patch?full_index=1",
        sha256="666eec8cfb0f71a87443ab27d179a9771bda32bcb8ff5e16afa3767f7b7f1e70",
        when="@:1.76%cce",
        level=2,
    )

    # Fix building with Intel compilers
    patch(
        "https://github.com/bfgroup/b2/commit/23212066f0f20358db54568bb16b3fe1d76f88ce.patch?full_index=1",
        sha256="4849671f9df4b8f3c962130d7f6d44eba3b20d113e84f9faade75e6469e90310",
        when="@1.77.0",
        working_dir="tools/build",
    )

    # Fix issues with PTHREAD_STACK_MIN not being a DEFINED constant in newer glibc
    # See https://github.com/spack/spack/issues/28273
    patch("pthread-stack-min-fix.patch", when="@1.69.0:1.72.0")

    # https://www.intel.com/content/www/us/en/developer/articles/technical/building-boost-with-oneapi.html
    patch("intel-oneapi-linux-jam.patch", when="@1.76: %oneapi")

    # https://github.com/spack/spack/issues/44003

    # https://github.com/boostorg/phoenix/issues/111

    # https://github.com/boostorg/filesystem/issues/284

    # https://github.com/boostorg/context/pull/280

    def patch(self):
        # Disable SSSE3 and AVX2 when using the NVIDIA compiler
        if self.spec.satisfies("%nvhpc"):
            filter_file("dump_avx2", "", "libs/log/build/Jamfile.v2")
