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
    patch("qt4-mac.patch", when="@4.8.7 platform=darwin")
    # https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=925811
    patch("qt4-qforeach.patch", when="@4 %gcc@9:")

    # Patches for qt@4:
    # https://github.com/spack/spack/issues/1517
    # https://bugreports.qt.io/browse/QTBUG-74196
    # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=89585

    # Patches for qt@5
    # https://bugreports.qt.io/browse/QTBUG-74219
    # https://bugreports.qt.io/browse/QTBUG-57656
    # https://bugreports.qt.io/browse/QTBUG-58038
    # https://codereview.qt-project.org/c/qt/qtbase/+/245425
    # https://github.com/Homebrew/homebrew-core/pull/5951
    # https://github.com/spack/spack/issues/14400
    # https://bugreports.qt.io/browse/QTBUG-78937
    # https://bugreports.qt.io/browse/QTBUG-93402
    # https://bugreports.qt.io/browse/QTBUG-84037
    # https://forum.qt.io/topic/130793/a-problem-with-python-path-when-i-try-to-build-qt-from-source-e-program-is-not-recognized-as-an-internal-or-external-command?_=1722965446110&lang=en-US

    # https://bugreports.qt.io/browse/QTBUG-90395
    # patch that adds missing `#include <cstdint>` in several files
    # required for gcc 13 (even though the original patch was developed for gcc 10)
    # (see https://gcc.gnu.org/gcc-13/porting_to.html)
    # https://github.com/microsoft/vcpkg/issues/21055
    # https://codereview.qt-project.org/c/qt/qtbase/+/503172
    conflicts("%apple-clang@15:", when="@:5.12.0")

    # Spack path substitution uses excessively long paths that exceed the hard-coded
    # limit of 256 used by teh generated code with the prefix path as string literals
    # causing qt to fail in ci.  This increases that limit to 1024.

    # with gcc@14: RapidJSON fails to build
    # https://github.com/Tencent/rapidjson/issues/2277
    # https://github.com/Tencent/rapidjson/pull/719

    # Do not define `wtf_ceil()` in MathExtras.h on macOS.
    # Prevents reference to removed API in order to avoid compilation errors
    # for webkit on macOS.

    conflicts("%gcc@10:", when="@5.9:5.12.6 +opengl")
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
            depends_on("sqlite+column_metadata", when="+sql", type=("build", "run"))
            depends_on("inputproto", when="@:5.8")
            depends_on("gmake", type="build")

    for plat in ["linux", "freebsd"]:
        with when(f"platform={plat} +gui"):
            depends_on("fontconfig")
            depends_on("libsm")
            depends_on("libx11")
            depends_on("libxcb")
            depends_on("libxkbcommon")
            depends_on("xcb-util-image")
            depends_on("xcb-util-keysyms")
            depends_on("xcb-util-renderutil")
            depends_on("xcb-util-wm")
            depends_on("libxext")
            depends_on("libxrender")

    for plat in ["linux", "freebsd", "windows"]:
        with when(f"platform={plat}"):
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
    depends_on("gtkplus", when="+gtk")

    depends_on("libpng@1.2.57", when="@3")
    depends_on("pcre+multibyte", when="@5.0:5.8")

    with when("+ssl"):
        depends_on("openssl")

    depends_on("libpng", when="@4:")
    depends_on("dbus", when="@4:+dbus")
    depends_on("gl", when="@4:+opengl")

    depends_on("harfbuzz", when="@5:")
    depends_on("double-conversion", when="@5.7:")
    depends_on("pcre2+multibyte", when="@5.9:")
    depends_on("llvm", when="@5.11: +doc")

    with when("+webkit"):


        with when("@5.7:"):

            depends_on("libxcomposite")
            depends_on("libxcursor")
            depends_on("libxi")
            depends_on("libxtst")
            depends_on("libxrandr")
            depends_on("libxdamage")
            depends_on("gettext")

    conflicts(
        "+webkit",
        when="@5.7:5.15",
        msg="qtwebengine@5.7:5.15 are based on Google Chromium versions which depend on Py2",
    )

    conflicts("+ssl", when="@:5.9")

    # gcc@4 is not supported as of Qt@5.14
    # https://doc.qt.io/qt-5.14/supported-platforms.html
    conflicts("%gcc@:4", when="@5.14:")

    # Compiling with oneAPI compilers icx, icpx requires patching
    # This has only been tested for 5.15.14 so far
    conflicts("%oneapi", when="@:5.15.13")

    # Mapping for compilers/systems in the QT 'mkspecs'
    compiler_mapping = {
        "intel-oneapi-compilers-classic": ("icc",),
        # This only works because we apply patch "qt51514-oneapi.patch"
        # above that replaces calls to "icc" with calls to "icx" in
        # qtbase/mkspecs/*
        "intel-oneapi-compilers": ("icc",),
        "aocc": ("clang-libc++", "clang"),
        "fj": ("clang",),
        "gcc": ("g++",),
    }
    platform_mapping = {"darwin": ("macx"), "windows": ("win32")}

    # webkit requires libintl (gettext), but does not test for it
    # correctly, so add it here.
    # Documentation generation requires the doc tools to be installed.
    # @when @run_after currently seems to ignore the 'when' restriction.
