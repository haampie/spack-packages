# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil
import sys
import tempfile

from spack_repo.builtin.build_systems.cmake import CMakePackage, generator

from spack.package import *

MACOS_VERSION = macos_version() if sys.platform == "darwin" else None


class QtPackage(CMakePackage):
    """Base package for Qt6 components"""

    homepage = "https://www.qt.io"

    @staticmethod
    def get_url(qualname):
        _url = "https://github.com/qt/{}/archive/refs/tags/v6.2.3.tar.gz"
        return _url.format(qualname.lower())

    @staticmethod
    def get_git(qualname):
        _git = "https://github.com/qt/{}.git"
        return _git.format(qualname.lower())

    @staticmethod
    def get_list_url(qualname):
        _list_url = "https://github.com/qt/{}/tags"
        return _list_url.format(qualname.lower())


    # Default dependencies for all qt-* components
    generator("ninja")

    # List of unnecessary directories in src/3rdparty
    vendor_deps_to_remove = []

    @run_after("patch")
    def remove_vendor_deps(self, vendor_dir, vendor_deps_to_remove):
        """Remove src/3rdparty libraries that are provided by spack"""
        vendor_dir = join_path(self.stage.source_path, "src", "3rdparty")
        with working_dir(vendor_dir):
            for dep in os.listdir():
                if os.path.isdir(dep):
                    if dep in vendor_deps_to_remove:
                        shutil.rmtree(dep)

    @staticmethod
    def _qt_feature_flag(feature):
        return f"FEATURE_{feature}"

    def define_qt_feature_from_variant(self, feature, variant=None):
        return self.define_from_variant(QtPackage._qt_feature_flag(feature), variant or feature)

    def define_qt_feature(self, feature, value=None):
        return self.define(QtPackage._qt_feature_flag(feature), value)

class QtBase(QtPackage):
    """Qt Base (Core, Gui, Widgets, Network, ...)"""

    url = QtPackage.get_url(__qualname__)
    list_url = QtPackage.get_list_url(__qualname__)


    variant("dbus", default=False, description="Build with D-Bus support.")
    variant(
        "framework", default=bool(MACOS_VERSION), description="Build as a macOS Framework package."
    )
    variant("gui", default=True, description="Build the Qt GUI module and dependencies.")
    variant("shared", default=True, description="Build shared libraries.")
    variant("sql", default=True, description="Build with SQL support.")
    variant("network", default=False, description="Build with SSL support.")

    # GUI-only dependencies
    variant(
        "accessibility",
        default=False,
        when="+gui",
        description="Build with accessibility support.",
    )
    variant("gtk", default=False, when="+gui", description="Build with gtkplus.")
    variant("opengl", default=False, when="+gui", description="Build with OpenGL support.")
    variant("widgets", default=True, when="+gui", description="Build with widgets.")


    # Dependencies, then variant- and version-specific dependencies
    depends_on("zstd")
    with when("platform=linux"):
        depends_on("libdrm")
        depends_on("at-spi2-core", when="+accessibility")

    with when("+gui"):
        with when("platform=linux"):
            depends_on("xcb-util-keysyms")
            depends_on("xcb-util-renderutil")
            depends_on("xcb-util-wm")

    with when("+network"):
        depends_on("openssl")
        with when("platform=linux"):
            depends_on("libproxy")

    # Qt6 requires newer compilers: see https://github.com/spack/spack/issues/34418
    conflicts("%gcc@:7")
    # The oldest compiler for Qt 6.5 is GCC 9: https://doc.qt.io/qt-6.5/supported-platforms.html
    with when("@6.5:"):
        conflicts("%gcc@:8")

    # ensure that Qt links against GSS framework on macOS: https://bugreports.qt.io/browse/QTBUG-114537
    with when("@6.3.2:6.5.1"):
        patch(
            "https://github.com/qt/qtbase/commit/c3d3e7312499189dde2ff9c0cb14bd608d6fd1cd.patch?full_index=1",
            sha256="85c16db15406b0094831bb57016dab7e0c0fd0978b082a1dc103c87334db7915",
        )
    with when("@6.3.2:6.5.2"):
        patch(
            "https://github.com/qt/qtbase/commit/1bf144ba78ff10d712b4de55d2797b9256948a1d.patch?full_index=1",
            sha256="e4d9f1aee0566558e77eef5609b63c1fde3f3986bea1b9d5d7930b297f916a5e",
        )

    vendor_deps_to_remove = [
        "double-conversion",
        "freetype",
        "harfbuzz-ng",
        "libjpeg",
        "libpng",
        "libpsl",
    ]

