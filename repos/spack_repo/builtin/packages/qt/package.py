# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import itertools
import os
import platform
import re
import sys
from typing import List

from spack_repo.builtin.build_systems.generic import Package

from spack.package import *

MACOS_VERSION = macos_version() if sys.platform == "darwin" else None
LINUX_VERSION = kernel_version() if platform.system() == "Linux" else None
IS_WINDOWS = sys.platform == "win32"


class Qt(Package):
    """Qt is a comprehensive cross-platform C++ application framework."""

    homepage = "https://qt.io"

    # Supported releases: 'https://download.qt.io/official_releases/qt/'
    # Older archives: 'https://download.qt.io/new_archive/qt/'
    url = "https://download.qt.io/archive/qt/5.15/5.15.2/single/qt-everywhere-src-5.15.2.tar.xz"
    list_url = "https://download.qt.io/archive/qt/"
    list_depth = 3

    phases = ["configure", "build", "install"]


    version("5.15.14", sha256="fdd3a4f197d2c800ee0085c721f4bef60951cbda9e9c46e525d1412f74264ed7")
    version("5.15.13", sha256="9550ec8fc758d3d8d9090e261329700ddcd712e2dda97e5fcfeabfac22bea2ca")
    version("5.15.12", sha256="93f2c0889ee2e9cdf30c170d353c3f829de5f29ba21c119167dee5995e48ccce")
    version("5.15.11", sha256="7426b1eaab52ed169ce53804bdd05dfe364f761468f888a0f15a308dc1dc2951")
    version("5.15.10", sha256="b545cb83c60934adc9a6bbd27e2af79e5013de77d46f5b9f5bb2a3c762bf55ca")
    version("5.15.5", sha256="5a97827bdf9fd515f43bc7651defaf64fecb7a55e051c79b8f80510d0e990f06")
    version("5.15.4", sha256="615ff68d7af8eef3167de1fd15eac1b150e1fd69d1e2f4239e54447e7797253b")
    version("5.9.9", sha256="5ce285209290a157d7f42ec8eb22bf3f1d76f2e03a95fc0b99b553391be01642")
    version("4.8.6", sha256="8b14dd91b52862e09b8e6a963507b74bc2580787d171feda197badfa7034032c")
    version("4.8.5", sha256="eb728f8268831dc4373be6403b7dd5d5dde03c169ad6882f9a8cb560df6aa138")
    version("3.3.8b", sha256="1b7a1ff62ec5a9cb7a388e2ba28fda6f960b27f27999482ebeceeadb72ac9f6e")

    variant("debug", default=False, description="Build debug version.")
    variant("dbus", default=False, description="Build with D-Bus support.")
    variant("doc", default=False, description="Build QDoc and documentation.")
    variant("examples", default=False, description="Build examples.")
    variant(
        "framework", default=bool(MACOS_VERSION), description="Build as a macOS Framework package."
    )
    variant("gtk", default=False, description="Build with gtkplus.")
    variant("gui", default=True, description="Build the Qt GUI module and dependencies")
    # Desktop only on Windows
    variant("opengl", default=False, description="Build with OpenGL support")
    for plat in ["linux", "darwin", "freebsd"]:
        with when(f"platform={plat}"):
            # webkit support requires qtquick2 which requires a GL implementation beyond what
            # windows system gl provides.
            # This is unavailable until we get a hardware accelerated option for EGL 2 on Windows
            # We can use llvm or angle for this, but those are not hardware accelerated, so are not
            # as useful for things like paraview
            variant("webkit", default=False, description="Build the Webkit extension")
    variant("location", default=False, description="Build the Qt Location module.")
    variant("phonon", default=False, description="Build with phonon support.")
    variant("shared", default=True, description="Build shared libraries.")
    variant("sql", default=True, description="Build with SQL support.")
    variant("ssl", default=True, description="Build with OpenSSL support.")
    variant("tools", default=True, description="Build tools, including Qt Designer.")

    provides("qmake")

    # Patches for qt@3
    patch("qt3-accept.patch", when="@3")
    patch("qt3-headers.patch", when="@3")

    # Patches for qt@4
    patch("qt4-configure-gcc.patch", when="@4:4.8.6 %gcc")
    patch("qt4-87-configure-gcc.patch", when="@4.8.7 %gcc")
    patch("qt4-tools.patch", when="@4+tools")
    # https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=925811

    # Patches for qt@4:
    # https://github.com/spack/spack/issues/1517
    # https://bugreports.qt.io/browse/QTBUG-74196
    # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=89585

    # Patches for qt@5
    # https://bugreports.qt.io/browse/QTBUG-74219
    # https://bugreports.qt.io/browse/QTBUG-57656
    # https://bugreports.qt.io/browse/QTBUG-58038
    patch("qt5-8-freetype.patch", when="@5.8.0 +gui")
    # https://codereview.qt-project.org/c/qt/qtbase/+/245425
    patch(
        "https://github.com/qt/qtbase/commit/a52d7861edfb5956de38ba80015c4dd0b596259b.patch?full_index=1",
        sha256="c113b4e31fc648d15d6d401f7625909d84f88320172bd1fbc5b100cc2cbf71e9",
        working_dir="qtbase",
        when="@5.10:5.12.0 %gcc@9:",
    )
    # https://github.com/Homebrew/homebrew-core/pull/5951
    patch("qt5-restore-pc-files.patch", when="@5.9:5.11 platform=darwin")
    # https://github.com/spack/spack/issues/14400
    # https://bugreports.qt.io/browse/QTBUG-78937
    # https://bugreports.qt.io/browse/QTBUG-93402
    patch("qt514.patch", when="@5.14")
    patch("qt514-isystem.patch", when="@5.14.2")
    # https://bugreports.qt.io/browse/QTBUG-84037
    patch("qt515-quick3d-assimp.patch", when="@5.15:5+opengl")
    # https://forum.qt.io/topic/130793/a-problem-with-python-path-when-i-try-to-build-qt-from-source-e-program-is-not-recognized-as-an-internal-or-external-command?_=1722965446110&lang=en-US
    patch("quote_qt515_masm_python.patch", when="@5.15:5.15.10 platform=windows")
    patch("quote_qt515_masm_script.patch", when="@5.15.11: platform=windows")
    patch("sfn_qt515_root_configure_path.patch", when="@5.15 platform=windows")
    patch("quote_qt515_foreign_types.patch", when="@5.15 platform=windows")

    # https://bugreports.qt.io/browse/QTBUG-90395
    # patch that adds missing `#include <cstdint>` in several files
    # required for gcc 13 (even though the original patch was developed for gcc 10)
    # (see https://gcc.gnu.org/gcc-13/porting_to.html)
    patch(
        "https://github.com/qt/qtbase/commit/cdf64b0e47115cc473e1afd1472b4b09e130b2a5.patch?full_index=1",
        sha256="2b881ffb2808f8fa79f51f8bec71be91a886bcdc59b1d7b6986cba26ed18d1d3",
        working_dir="qtbase",
        when="@5.12.1: %apple-clang@15:",
    )

    # Spack path substitution uses excessively long paths that exceed the hard-coded
    # limit of 256 used by teh generated code with the prefix path as string literals
    # causing qt to fail in ci.  This increases that limit to 1024.

    # with gcc@14: RapidJSON fails to build
    # https://github.com/Tencent/rapidjson/issues/2277
    # https://github.com/Tencent/rapidjson/pull/719

    # Do not define `wtf_ceil()` in MathExtras.h on macOS.
    # Prevents reference to removed API in order to avoid compilation errors
    # for webkit on macOS.

    conflicts("%gcc@11:", when="@5.8")
    conflicts("%apple-clang@13:", when="@:5.13")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # Build-only dependencies
    for plat in ["linux", "darwin", "freebsd"]:
        with when(f"platform={plat}"):
            depends_on("pkgconfig", type="build")
            depends_on("libsm", when="@3")
            depends_on("glib", when="@4:")
            depends_on("libmng")
            depends_on("assimp@5.0.0:5", when="@5.5:+opengl")

    for plat in ["linux", "freebsd"]:
        with when(f"platform={plat} +gui"):
            depends_on("libsm")
            depends_on("libx11")
            depends_on("libxcb")
            depends_on("libxkbcommon")
            depends_on("xcb-util-image")
            conflicts("+framework", msg="QT cannot be built as a framework except on macOS.")

    with when("platform=windows +sql"):
        # Windows sqlite has no column_metadata variant unlike all other platforms
        depends_on("sqlite", type=("build", "run"))

    with when("platform=darwin"):
        conflicts("@:4.8.6", msg="QT 4 for macOS is only patched for 4.8.7")
        conflicts(
            "target=aarch64:",
            when="@:5.15.3",
            msg="Apple Silicon requires a very new version of qt",
        )

    depends_on("python", when="@5.7.0:", type="build")

    # Dependencies, then variant- and version-specific dependencies
    depends_on("zlib-api")
    depends_on("freetype", when="+gui")


    with when("+ssl"):
        depends_on("openssl@1.1.1:", when="@5.15.0:")


    depends_on("double-conversion", when="@5.7:")
    depends_on("pcre2+multibyte", when="@5.9:")
    depends_on("llvm", when="@5.11: +doc")
    depends_on("zstd@1.3:", when="@5.13:")

    with when("+webkit"):
        patch(
            "https://src.fedoraproject.org/rpms/qt5-qtwebengine/raw/32062243e895612823b47c2ae9eeb873a98a3542/f/qtwebengine-gcc11.patch",
            sha256="14e2d6baff0d09a528ee3e2b5a14de160859880360100af75ea17f3e0f672787",
            working_dir="qtwebengine",
            when="@5.15.2: %gcc@11:",
        )
        # the gl headers and dbus are needed to build webkit
        conflicts("~opengl")
        conflicts("~dbus")

        depends_on("flex", type="build")
        depends_on("bison", type="build")
        depends_on("gperf")

        with when("@5.10:"):
            depends_on("nss@3.62:")

        with when("@5.7:"):
            # https://www.linuxfromscratch.org/blfs/view/svn/x/qtwebengine.html
            depends_on("ninja", type="build")

        # https://doc.qt.io/qt-5.15/qtwebengine-platform-notes.html
        with when("@5.7: platform=linux"):
            depends_on("libdrm")
            depends_on("libxcomposite")
            depends_on("libxcursor")



    # gcc@4 is not supported as of Qt@5.14
    # https://doc.qt.io/qt-5.14/supported-platforms.html

    # Compiling with oneAPI compilers icx, icpx requires patching
    # This has only been tested for 5.15.14 so far
    conflicts("%oneapi", when="@:5.15.13")
    patch("qt51514-oneapi.patch", when="@5.15.14: %oneapi")

    # Mapping for compilers/systems in the QT 'mkspecs'
    compiler_mapping = {
        "intel-oneapi-compilers-classic": ("icc",),
        # This only works because we apply patch "qt51514-oneapi.patch"
        # above that replaces calls to "icc" with calls to "icx" in
        # qtbase/mkspecs/*
        "intel-oneapi-compilers": ("icc",),
        "apple-clang": ("clang-libc++", "clang"),
        "clang": ("clang-libc++", "clang"),
        "aocc": ("clang-libc++", "clang"),
        "fj": ("clang",),
        "gcc": ("g++",),
    }
    platform_mapping = {"darwin": ("macx"), "windows": ("win32")}

    # webkit requires libintl (gettext), but does not test for it
    # correctly, so add it here.
    # Documentation generation requires the doc tools to be installed.
    # @when @run_after currently seems to ignore the 'when' restriction.
