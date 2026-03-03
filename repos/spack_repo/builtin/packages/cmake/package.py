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

    version("4.1.5", sha256="50ce77215cf266630fa5de97c360f4c313bb79f94b35236b63c1216de3196356")
    version("4.1.2", sha256="643f04182b7ba323ab31f526f785134fb79cba3188a852206ef0473fee282a15")
    version("4.1.1", sha256="b29f6f19733aa224b7763507a108a427ed48c688e1faf22b29c44e1c30549282")
    version("4.0.6", sha256="9ebe11be8d304336d62a3e71ca36c18f0a4e40036b97c533d63cf730364b6528")
    version("4.0.4", sha256="629be82af0b76e029b675a4a37569e2ddc1769d42a768957c00ec0e98407737e")
    version("2.8.10.2", sha256="ce524fb39da06ee6d47534bbcec6e0b50422e18b62abc4781a4ba72ea2910eb1")

    with default_args(deprecated=True):
        version("4.1.0", sha256="81ee8170028865581a8e10eaf055afb620fa4baa0beb6387241241a975033508")
        version("4.0.3", sha256="8d3537b7b7732660ea247398f166be892fe6131d63cc291944b45b91279f3ffb")
        version("4.0.0", sha256="ddc54ad63b87e153cf50be450a6580f1b17b4881de8941da963ff56991a4083b")
        version(
            "3.31.8", sha256="e3cde3ca83dc2d3212105326b8f1b565116be808394384007e7ef1c253af6caa"
        )
        version(
            "3.31.6", sha256="653427f0f5014750aafff22727fb2aa60c6c732ca91808cfb78ce22ddd9e55f0"
        )

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    variant(
        "build_type",
        default="Release",
        description="CMake build type",
        values=("Debug", "Release", "RelWithDebInfo", "MinSizeRel"),
    )

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

    # Revert the change that introduced a regression when parsing mpi link
    # flags, see: https://gitlab.kitware.com/cmake/cmake/issues/19516

    # Fix linker error when using external libs on darwin.
    # See https://gitlab.kitware.com/cmake/cmake/merge_requests/2873

    # Fix builds with XLF + Ninja generator
    # https://gitlab.kitware.com/cmake/cmake/merge_requests/4075

    # Statically linked binaries error on install when CMAKE_INSTALL_RPATH is set
    # https://gitlab.kitware.com/cmake/cmake/-/merge_requests/9623


    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("ninja", when="platform=windows")
    depends_on("gmake", type=("build", "run"), when="platform=linux")
    depends_on("gmake", type=("build", "run"), when="platform=darwin")
    depends_on("gmake", type=("build", "run"), when="platform=freebsd")

    depends_on("qt", when="+qtgui")
    # Qt depends on libmng, which is a CMake package;
    # ensure we build using a non CMake build system
    # when libmng is build as a transitive dependency of CMake
    for plat in ["linux", "darwin", "freebsd"]:
        with when(f"platform={plat}"):
            depends_on("libmng build_system=autotools", when="+qtgui")

    # See https://gitlab.kitware.com/cmake/cmake/-/issues/21135
    conflicts(
        "platform=darwin %gcc",
        when="@:3.17",
        msg="CMake <3.18 does not compile with GCC on macOS, "
        "please use %apple-clang or a newer CMake release. "
        "See: https://gitlab.kitware.com/cmake/cmake/-/issues/21135",
    )

    # Vendored dependencies do not build with nvhpc; it's also more
    # transparent to patch Spack's versions of CMake's dependencies.
    conflicts("+ownlibs %nvhpc")

    # Use Spack's curl even if +ownlibs, since that allows us to make use of
    # the conflicts on the curl package for TLS libs like OpenSSL.
    # In the past we let CMake build a vendored copy of curl, but had to
    # provide Spack's TLS libs anyways, which is not flexible, and actually
    # leads to issues where we have to keep track of the vendored curl version
    # and its conflicts with OpenSSL.
    depends_on("curl@:8.15", when="@:3.25")
    depends_on("curl")

    # https://gitlab.kitware.com/cmake/cmake/-/merge_requests/11134
    conflicts("curl@8.16:", when="@:3.30")

    # When using curl, cmake defaults to using system zlib too, probably because
    # curl already depends on zlib. Therefore, also unconditionaly depend on zlib.
    depends_on("zlib-api")

    with when("~ownlibs"):
        depends_on("expat")
        for plat in ["darwin", "linux", "freebsd"]:
            with when("platform=%s" % plat):
                depends_on("libarchive@3.3.3:", when="@3.15.0:")
                depends_on("libuv@1.0.0:1.10", when="@3.7.0:3.10.3")
                depends_on("libuv@1.10.0:1.10", when="@3.11.0:3.11")
    with when("+doc"):
        depends_on("python@2.7.11:", type="build")
        depends_on("py-sphinx", type="build")

    # Cannot build with Intel, should be fixed in 3.6.2
    # https://gitlab.kitware.com/cmake/cmake/issues/16226

    # Cannot build with Intel again, should be fixed in 3.17.4 and 3.18.1
    # https://gitlab.kitware.com/cmake/cmake/-/issues/21013

    # https://gitlab.kitware.com/cmake/cmake/issues/18232

    # Cray libhugetlbfs and icpc warnings failing CXX tests
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

    # https://gitlab.kitware.com/cmake/cmake/issues/18166

    resource(
        name="cmake-bootstrap",
        url="https://cmake.org/files/v3.21/cmake-3.21.2-windows-x86_64.zip",
        checksum="213a4e6485b711cb0a48cbd97b10dfe161a46bfe37b8f3205f47e99ffec434d2",
        placement="cmake-bootstrap",
        when="@3.0.2: platform=windows",
    )

    resource(
        name="cmake-bootstrap",
        url="https://cmake.org/files/v2.8/cmake-2.8.4-win32-x86.zip",
        checksum="8b9b520f3372ce67e33d086421c1cb29a5826d0b9b074f44a8a0304e44cf88f3",
        placement="cmake-bootstrap",
        when="@:2.8.10.2 platform=windows",
    )

    phases = ["bootstrap", "build", "install"]

    def test_cmake(self):
        """check version from cmake"""
        self.run_version_check("cmake")

