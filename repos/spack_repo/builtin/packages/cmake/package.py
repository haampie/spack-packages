# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pathlib
import re
import sys

from spack_repo.builtin.build_systems.generic import Package

from spack.package import *


class Cmake(Package):
    """A cross-platform, open-source build system. CMake is a family of
    tools designed to build, test and package software.
    """

    homepage = "https://www.cmake.org"
    url = "https://github.com/Kitware/CMake/releases/download/v3.19.0/cmake-3.19.0.tar.gz"
    git = "https://gitlab.kitware.com/cmake/cmake.git"
    github = "https://github.com/kitware/cmake"


    tags = ["build-tools", "windows"]

    executables = ["^cmake[0-9]*$"]


    version("3.4.3", sha256="b73f8c1029611df7ed81796bf5ca8ba0ef41c6761132340c73ffe42704f980fa")

    with default_args(deprecated=True):
        version("4.1.0", sha256="81ee8170028865581a8e10eaf055afb620fa4baa0beb6387241241a975033508")
        version("4.0.3", sha256="8d3537b7b7732660ea247398f166be892fe6131d63cc291944b45b91279f3ffb")
        version("4.0.0", sha256="ddc54ad63b87e153cf50be450a6580f1b17b4881de8941da963ff56991a4083b")



    # We default ownlibs to true because it greatly speeds up the CMake
    # build, and CMake is built frequently. Also, CMake is almost always
    # a build dependency, and its libs will not interfere with others in
    # the build.
    variant("ownlibs", default=True, description="Use CMake-provided third-party libraries")
    variant(
        "doc",
        default=False,
        description="Enables the generation of html and man page documentation",
    )
    variant("qtgui", default=False, description="Enables the build of the Qt GUI")

    for spack_platform in ["freebsd", "linux", "darwin"]:
        with when(f"platform={spack_platform}"):
            variant("ncurses", default=True, description="Enables the build of the ncurses gui")

    # Fix builds with XLF + Ninja generator
    # https://gitlab.kitware.com/cmake/cmake/merge_requests/4075
    # Statically linked binaries error on install when CMAKE_INSTALL_RPATH is set
    # https://gitlab.kitware.com/cmake/cmake/-/merge_requests/9623



    depends_on("gmake", type=("build", "run"), when="platform=darwin")
    depends_on("qt", when="+qtgui")
    # ensure we build using a non CMake build system
    # when libmng is build as a transitive dependency of CMake
    for plat in ["linux", "darwin", "freebsd"]:
        with when(f"platform={plat}"):
            depends_on("libmng build_system=autotools", when="+qtgui")
    # See https://gitlab.kitware.com/cmake/cmake/-/issues/21135

    # Vendored dependencies do not build with nvhpc; it's also more
    # transparent to patch Spack's versions of CMake's dependencies.

    # Use Spack's curl even if +ownlibs, since that allows us to make use of
    # the conflicts on the curl package for TLS libs like OpenSSL.
    # In the past we let CMake build a vendored copy of curl, but had to
    # provide Spack's TLS libs anyways, which is not flexible, and actually
    # leads to issues where we have to keep track of the vendored curl version
    # and its conflicts with OpenSSL.

    # https://gitlab.kitware.com/cmake/cmake/-/merge_requests/11134

    # When using curl, cmake defaults to using system zlib too, probably because
    # curl already depends on zlib. Therefore, also unconditionaly depend on zlib.

    with when("~ownlibs"):
        depends_on("expat")
        for plat in ["darwin", "linux", "freebsd"]:
            with when("platform=%s" % plat):
                depends_on("libarchive@3.1.0: xar=expat compression=bz2lib,lzma,zlib,zstd")

    with when("+doc"):
        depends_on("py-sphinx", type="build")
    # Cannot build with Intel, should be fixed in 3.6.2
    # https://gitlab.kitware.com/cmake/cmake/issues/18232

    # https://gitlab.kitware.com/cmake/cmake/-/merge_requests/4698
    # https://gitlab.kitware.com/cmake/cmake/-/merge_requests/4681

    # The Fujitsu compiler requires the '--linkfortran' option
    # to combine C++ and Fortran programs.

    # Remove -A from the C++ flags we use when CXX_EXTENSIONS is OFF
    # Should be fixed in 3.19. This patch is needed also for nvhpc.
    # https://gitlab.kitware.com/cmake/cmake/-/merge_requests/5025

    # Adds CCE v11+ fortran preprocessing definition.
    # requires Cmake 3.19+
    # https://gitlab.kitware.com/cmake/cmake/-/merge_requests/5882
    patch(
        "5882-enable-cce-fortran-preprocessing.patch",
        sha256="b48396c0e4f61756248156b6cebe9bc0d7a22228639b47b5aa77c9330588ce88",
        when="@3.19.0:3.19",
    )

    # https://gitlab.kitware.com/cmake/cmake/issues/18166



    phases = ["bootstrap", "build", "install"]

    def patch(self):
        # https://github.com/Kitware/CMake/commit/c8143074cf3954b1e169904eb9d843cfbe14acc3
        if self.spec.satisfies("@2.8,3.2:3.31.8,4.0:4.0.3,4.1:4.1.1"):
            filter_file(
                "curl_proxytype HTTPProxyType;",
                "long HTTPProxyType;",
                "Source/CTest/cmCTestCurl.h",
                string=True,
            )

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"cmake.*version\s+(\S+)", output)
