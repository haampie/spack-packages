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

    version("develop", branch="develop", submodules=True)
    version("1.89.0", sha256="85a33fa22621b4f314f8e85e1a5e2a9363d22e4f4992925d4bb3bc631b5a0c7a")
    version("1.88.0", sha256="46d9d2c06637b219270877c9e16155cbd015b6dc84349af064c088e9b5b12f7b")
    version("1.87.0", sha256="af57be25cb4c4f4b413ed692fe378affb4352ea50fbe294a11ef548f4d527d89")
    version("1.86.0", sha256="1bed88e40401b2cb7a1f76d4bab499e352fa4d0c5f31c0dbae64e24d34d7513b")
    version("1.85.0", sha256="7009fe1faa1697476bdc7027703a2badb84e849b7b0baad5086b087b971f8617")
    version("1.84.0", sha256="cc4b893acf645c9d4b698e9a0f08ca8846aa5d6c68275c14c3e7949c24109454")
    version("1.83.0", sha256="6478edfe2f3305127cffe8caf73ea0176c53769f4bf1585be237eb30798c3b8e")
    version("1.82.0", sha256="a6e1ab9b0860e6a2881dd7b21fe9f737a095e5f33a3a874afc6a345228597ee6")
    version("1.81.0", sha256="71feeed900fbccca04a3b4f2f84a7c217186f28a940ed8b7ed4725986baf99fa")
    version("1.80.0", sha256="1e19565d82e43bc59209a168f5ac899d3ba471d55c7610c677d4ccf2c9c500c0")
    version("1.79.0", sha256="475d589d51a7f8b3ba2ba4eda022b170e562ca3b760ee922c146b6c65856ef39")
    version("1.78.0", sha256="8681f175d4bdb26c52222665793eef08490d7758529330f98d3b29dd0735bccc")
    version("1.77.0", sha256="fc9f85fc030e233142908241af7a846e60630aa7388de9a5fafb1f3a26840854")
    version("1.76.0", sha256="f0397ba6e982c4450f27bf32a2a83292aba035b827a5623a14636ea583318c41")
    version("1.75.0", sha256="953db31e016db7bb207f11432bef7df100516eeb746843fa0486a222e3fd49cb")
    version("1.74.0", sha256="83bfc1507731a0906e387fc28b7ef5417d591429e51e788417fe9ff025e116b1")
    version("1.73.0", sha256="4eb3b8d442b426dc35346235c8733b5ae35ba431690e38c6a8263dce9fcbb402")
    version("1.72.0", sha256="59c9b274bc451cf91a9ba1dd2c7fdcaf5d60b1b3aa83f2c9fa143417cc660722")
    version("1.71.0", sha256="d73a8da01e8bf8c7eda40b4c84915071a8c8a0df4a6734537ddde4a8580524ee")
    version("1.70.0", sha256="430ae8354789de4fd19ee52f3b1f739e1fba576f0aded0897c3c2bc00fb38778")
    version("1.69.0", sha256="8f32d4617390d1c2d16f26a27ab60d97807b35440d45891fa340fc2648b04406")
    version("1.68.0", sha256="7f6130bc3cf65f56a618888ce9d5ea704fa10b462be126ad053e80e553d6d8b7")
    version("1.67.0", sha256="2684c972994ee57fc5632e03bf044746f6eb45d4920c343937a465fd67a5adba")
    version("1.66.0", sha256="5721818253e6a0989583192f96782c4a98eb6204965316df9f5ad75819225ca9")
    version("1.65.1", sha256="9807a5d16566c57fd74fb522764e0b134a8bbe6b6e8967b83afefd30dcd3be81")
    version("1.65.0", sha256="ea26712742e2fb079c2a566a31f3266973b76e38222b9f88b387e3c8b2f9902c")
    version("1.64.0", sha256="7bcc5caace97baa948931d712ea5f37038dbb1c5d89b43ad4def4ed7cb683332")
    version("1.63.0", sha256="beae2529f759f6b3bf3f4969a19c2e9d6f0c503edcb2de4a61d1428519fcb3b0")
    version("1.62.0", sha256="36c96b0f6155c98404091d8ceb48319a28279ca0333fba1ad8611eb90afb2ca0")
    version("1.61.0", sha256="a547bd06c2fd9a71ba1d169d9cf0339da7ebf4753849a8f7d6fdb8feee99b640")
    version("1.60.0", sha256="686affff989ac2488f79a97b9479efb9f2abae035b5ed4d8226de6857933fd3b")
    version("1.59.0", sha256="727a932322d94287b62abb1bd2d41723eec4356a7728909e38adb65ca25241ca")
    version("1.58.0", sha256="fdfc204fc33ec79c99b9a74944c3e54bd78be4f7f15e260c0e2700a36dc7d3e5")
    version("1.57.0", sha256="910c8c022a33ccec7f088bd65d4f14b466588dda94ba2124e78b8c57db264967")
    version("1.56.0", sha256="134732acaf3a6e7eba85988118d943f0fa6b7f0850f65131fff89823ad30ff1d")
    version("1.55.0", sha256="fff00023dd79486d444c8e29922f4072e1d451fc5a4d2b6075852ead7f2b7b52")
    version("1.54.0", sha256="047e927de336af106a24bceba30069980c191529fd76b8dff8eb9a328b48ae1d")
    version("1.53.0", sha256="f88a041b01882b0c9c5c05b39603ec8383fb881f772f6f9e6e6fd0e0cddb9196")
    version("1.52.0", sha256="222b6afd7723f396f5682c20130314a10196d3999feab5ba920d2a6bf53bac92")
    version("1.51.0", sha256="fb2d2335a29ee7fe040a197292bfce982af84a645c81688a915c84c925b69696")
    version("1.50.0", sha256="c9ace2b8c81fa6703d1d17c7e478de3bc51101c5adbdeb3f6cb72cf3045a8529")
    version("1.49.0", sha256="dd748a7f5507a7e7af74f452e1c52a64e651ed1f7263fce438a06641d2180d3c")
    version("1.48.0", sha256="1bf254b2d69393ccd57a3cdd30a2f80318a005de8883a0792ed2f5e2598e5ada")
    version("1.47.0", sha256="815a5d9faac4dbd523fbcf3fe1065e443c0bbf43427c44aa423422c6ec4c2e31")
    version("1.46.1", sha256="e1dfbf42b16e5015c46b98e9899c423ca4d04469cbeee05e43ea19236416d883")
    version("1.46.0", sha256="2f90f60792fdc25e674b8a857a0bcbb8d01199651719c90d5c4f8c61c08eba59")
    version("1.45.0", sha256="55ed3ec51d5687e8224c988e22bef215dacce04e037d9f689569a80c4377a6d5")
    version("1.44.0", sha256="45c328029d97d1f1dc7ff8c9527cd0c5cc356636084a800bca2ee4bfab1978db")
    version("1.43.0", sha256="344f100b1aa410e812cabf0e4130728a80be042bf346135516b9187853806120")
    version("1.42.0", sha256="4b1eb95bd250ce15ac66435d6167f225b072b0d3a7eb72477a31847a9ca9e609")
    version("1.41.0", sha256="1ef94e6749eaf13318284b4f629be063544c7015b45e38113b975ac1945cc726")
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
    variant(
        "visibility",
        values=("global", "protected", "hidden"),
        default="hidden",
        multi=False,
        description="Default symbol visibility in compiled libraries (1.69.0 or later)",
    )

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    # Unicode support
    depends_on("icu4c", when="+icu")
    depends_on("icu4c cxxstd=11", when="+icu cxxstd=11")
    depends_on("icu4c cxxstd=14", when="+icu cxxstd=14")
    depends_on("icu4c cxxstd=17", when="+icu cxxstd=17")
    conflicts("cxxstd=98", when="+icu")  # Requires c++11 at least
    conflicts("+locale ~icu")  # Boost.Locale "strongly recommends" icu, so enforce it

    depends_on("python", when="+python")
    # https://github.com/boostorg/python/commit/cbd2d9f033c61d29d0a1df14951f4ec91e7d05cd
    depends_on("python@:3.9", when="@:1.75 +python")

    depends_on("mpi", when="+mpi")
    depends_on("bzip2", when="+iostreams")
    depends_on("zlib-api", when="+iostreams")
    depends_on("zstd", when="+iostreams")
    depends_on("xz", when="+iostreams")
    depends_on("py-numpy", when="+numpy", type=("build", "run"))
    # https://github.com/boostorg/python/issues/431
    depends_on("py-numpy@:1", when="@:1.86+numpy", type=("build", "run"))

    # Improve the error message when the context-impl variant is conflicting
    conflicts("context-impl=fcontext", when="@:1.65.0")
    conflicts("context-impl=ucontext", when="@:1.65.0")
    conflicts("context-impl=winfib", when="@:1.65.0")

    # Coroutine, Context, Fiber, etc., are not straightforward.
    conflicts("+context", when="@:1.50")  # Context since 1.51.0.
    conflicts("cxxstd=98", when="+context")  # Context requires >=C++11.
    conflicts("+coroutine", when="@:1.52")  # Context since 1.53.0.
    conflicts("~context", when="+coroutine")  # Coroutine requires Context.
    conflicts("+fiber", when="@:1.61")  # Fiber since 1.62.0.
    conflicts("cxxstd=98", when="+fiber")  # Fiber requires >=C++11.
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
    conflicts("%gcc", when="@:1.76 +system platform=darwin")

    # Boost 1.80 does not build with the Intel oneapi compiler
    # (https://github.com/spack/spack/pull/32879#issuecomment-1265933265)
    conflicts("%oneapi", when="@1.80")

    # Boost did not support the oneapi compilers prior to 1.76
    conflicts("%oneapi@2023:", when="@:1.75")

    # Boost 1.85.0 stacktrace added a hard compilation error that has to
    # explicitly be suppressed on some platforms:
    # https://github.com/boostorg/stacktrace/pull/150. This conflict could be
    # turned into a variant that allows users to opt-in when they know it is
    # safe to do so on affected platforms.
    conflicts("+clanglibcpp", when="@1.85: +stacktrace")

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
    patch(
        "https://www.boost.org/patches/1_82_0/0002-filesystem-fix-win-smbv1-dir-iterator.patch",
        sha256="738ba8e0d7b5cdcf5fae4998f9450b51577bbde1bb0d220a0721551609714ca4",
        when="@1.82.0 platform=windows",
    )

    # https://github.com/boostorg/context/pull/280
    patch(
        "https://github.com/boostorg/context/commit/d11cbccc87da5d6d41c04f3949e18d49c43e62fc.patch?full_index=1",
        sha256="e2d37f9e35e8e238977de9af32604a8e1c2648d153df1d568935a20216b5c67f",
        when="@1.87.0",
        working_dir="libs/context",
    )

