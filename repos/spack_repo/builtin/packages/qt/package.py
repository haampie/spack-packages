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

    version("5.15.17", sha256="85eb566333d6ba59be3a97c9445a6e52f2af1b52fc3c54b8a2e7f9ea040a7de4")
    version("5.15.16", sha256="efa99827027782974356aceff8a52bd3d2a8a93a54dd0db4cca41b5e35f1041c")
    version("5.15.15", sha256="b423c30fe3ace7402e5301afbb464febfb3da33d6282a37a665be1e51502335e")
    version("5.15.14", sha256="fdd3a4f197d2c800ee0085c721f4bef60951cbda9e9c46e525d1412f74264ed7")
    version("5.15.13", sha256="9550ec8fc758d3d8d9090e261329700ddcd712e2dda97e5fcfeabfac22bea2ca")
    version("5.15.12", sha256="93f2c0889ee2e9cdf30c170d353c3f829de5f29ba21c119167dee5995e48ccce")
    version("5.15.11", sha256="7426b1eaab52ed169ce53804bdd05dfe364f761468f888a0f15a308dc1dc2951")
    version("5.15.10", sha256="b545cb83c60934adc9a6bbd27e2af79e5013de77d46f5b9f5bb2a3c762bf55ca")
    version("5.15.9", sha256="26d5f36134db03abe4a6db794c7570d729c92a3fc1b0bf9b1c8f86d0573cd02f")
    version("5.15.8", sha256="776a9302c336671f9406a53bd30b8e36f825742b2ec44a57c08217bff0fa86b9")
    version("5.15.7", sha256="8a71986676a3f37a198a9113acedbfd5bc5606a459b6b85816d951458adbe9a0")
    version("5.15.6", sha256="ebc77d27934b70b25b3dc34fbec7c4471eb451848e891c42b32409ea30fe309f")
    version("5.15.5", sha256="5a97827bdf9fd515f43bc7651defaf64fecb7a55e051c79b8f80510d0e990f06")
    version("5.15.4", sha256="615ff68d7af8eef3167de1fd15eac1b150e1fd69d1e2f4239e54447e7797253b")
    version("5.15.3", sha256="b7412734698a87f4a0ae20751bab32b1b07fdc351476ad8e35328dbe10efdedb")
    version("5.15.2", sha256="3a530d1b243b5dec00bc54937455471aaa3e56849d2593edb8ded07228202240")
    version("5.14.2", sha256="c6fcd53c744df89e7d3223c02838a33309bd1c291fcb6f9341505fe99f7f19fa")
    version("5.12.10", sha256="3e0ee1e57f5cf3eeb038d0b4b22c7eb442285c62639290756b39dc93a1d0e14f")
    version("5.9.9", sha256="5ce285209290a157d7f42ec8eb22bf3f1d76f2e03a95fc0b99b553391be01642")
    version("5.6.3", sha256="2fa0cf2e5e8841b29a4be62062c1a65c4f6f2cf1beaf61a5fd661f520cd776d0")
    version("5.3.2", sha256="c8d3fd2ead30705c6673c5e4af6c6f3973346b4fb2bd6079c7be0943a5b0282d")
    version("5.2.1", sha256="84e924181d4ad6db00239d87250cc89868484a14841f77fb85ab1f1dbdcd7da1")
    version("4.8.7", sha256="e2882295097e47fe089f8ac741a95fef47e0a73a3f3cdf21b56990638f626ea0")
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

    # Dependencies, then variant- and version-specific dependencies
    depends_on("icu4c")
    depends_on("jpeg")
    depends_on("libtiff")
    depends_on("libxml2")
    depends_on("zlib-api")
    depends_on("freetype", when="+gui")
    depends_on("gtkplus", when="+gtk")

    depends_on("libpng@1.2.57", when="@3")
    depends_on("pcre+multibyte", when="@5.0:5.8")

    with when("+ssl"):
        depends_on("openssl")
        depends_on("openssl@1.1.1:", when="@5.15.0:")

    depends_on("libpng", when="@4:")
    depends_on("dbus", when="@4:+dbus")
    depends_on("gl", when="@4:+opengl")

    depends_on("harfbuzz", when="@5:")
    depends_on("double-conversion", when="@5.7:")
    depends_on("pcre2+multibyte", when="@5.9:")
    depends_on("llvm", when="@5.11: +doc")
    depends_on("zstd@1.3:", when="@5.13:")

    with when("+webkit"):
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
