# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import shutil
import sys

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Hdf5(CMakePackage):
    """HDF5 is a data model, library, and file format for storing and managing
    data. It supports an unlimited variety of datatypes, and is designed for
    flexible and efficient I/O and for high volume and complex data.
    """

    homepage = "https://support.hdfgroup.org"
    url = "https://support.hdfgroup.org/releases/hdf5/v1_14/v1_14_5/downloads/hdf5-1.14.5.tar.gz"

    git = "https://github.com/HDFGroup/hdf5.git"

    tags = ["e4s", "windows"]
    executables = ["^h5cc$", "^h5pcc$"]

    test_requires_compiler = True


    # The 'develop' version is renamed so that we could uninstall (or patch) it
    # without affecting other develop version.

    # Odd versions are considered experimental releases
    # Even versions are maintenance versions
    version(
        "1.14.6",
        sha256="e4defbac30f50d64e1556374aa49e574417c9e72c6b1de7a4ff88c4b1bea6e9b",
        url="https://support.hdfgroup.org/releases/hdf5/v1_14/v1_14_6/downloads/hdf5-1.14.6.tar.gz",
        preferred=True,
    )
    version(
        "1.14.4-3",
        sha256="019ac451d9e1cf89c0482ba2a06f07a46166caf23f60fea5ef3c37724a318e03",
        url="https://support.hdfgroup.org/releases/hdf5/v1_14/v1_14_4/downloads/hdf5-1.14.4-3.tar.gz",
    )
    version("1.12.3", sha256="c15adf34647918dd48150ea1bd9dffd3b32a3aec5298991d56048cc3d39b4f6f")
    version("1.12.2", sha256="2a89af03d56ce7502dcae18232c241281ad1773561ec00c0f0e8ee2463910f14")
    version("1.10.5", sha256="6d4ce8bf902a97b050f6f491f4268634e252a63dadd6656a1a9be5b7b7726fa8")
    version("1.10.4", sha256="8f60dc4dd6ab5fcd23c750d1dc5bca3d0453bdce5c8cdaf0a4a61a9d1122adb2")
    version("1.10.0", sha256="81f6201aba5c30dced5dcd62f5d5477a2790fd5850e02ac514ca8bf3e2bb375a")
    version("1.8.23", sha256="37fa4eb6cd0e181eb49a10d54611cb00700e9537f805d03e6853503afe5abc27")
    variant("shared", default=True, description="Builds a shared version of the library")

    variant("hl", default=False, description="Enable the high-level library")
    variant("cxx", default=False, description="Enable C++ support")
    variant("map", when="@1.14:", default=False, description="Enable MAP API support")
    variant(
        "subfiling", when="@1.14: +mpi", default=False, description="Enable Subfiling VFD support"
    )
    variant("fortran", default=False, description="Enable Fortran support")
    variant("java", when="@1.10:", default=False, description="Enable Java support")
    variant("threadsafe", default=False, description="Enable thread-safe capabilities")
    variant("tools", default=True, description="Enable building tools")
    variant("mpi", default=True, description="Enable MPI support")
    variant("szip", default=False, description="Enable szip support")
    # Build HDF5 with API compatibility.
    variant(
        "api",
        default="default",
        description="Choose api compatibility for earlier version",
        values=("default", "v200", "v114", "v112", "v110", "v18", "v16"),
        multi=False,
    )

    depends_on("c", type="build")
    depends_on("cxx", type="build", when="+cxx")
    depends_on("fortran", type="build", when="+fortran")

    depends_on("cmake@3.12:", type="build")
    depends_on("cmake@3.18:", type="build", when="@1.14:")
    depends_on("cmake@3.26:", type="build", when="@2.0:")

    with when("+mpi"):
        depends_on("mpi")
        depends_on("mpich+fortran", when="+fortran ^[virtuals=mpi] mpich")

    depends_on("java", type=("build", "run"), when="+java")
    depends_on("szip", when="+szip")

    depends_on("zlib-api")
    # See https://github.com/HDFGroup/hdf5/pull/4147
    depends_on(
        "zlib-ng~new_strategies",
        when="@:1.14.3,develop-1.8:develop-1.12 ^[virtuals=zlib-api] zlib-ng",
    )

    # The compiler wrappers (h5cc, h5fc, etc.) run 'pkg-config'.
    # Skip this on Windows since pkgconfig is autotools
    for plat in ["darwin", "linux"]:
        depends_on("pkgconfig", when=f"platform={plat}", type="run")

    conflicts("+mpi", "^mpich@4.0:4.0.3")
    conflicts("api=v200", when="@1.6:1.14", msg="v200 is not compatible with this release")
    conflicts(
        "api=v112",
        when="@develop-1.8:develop-1.10",
        msg="v112 is not compatible with this release",
    )

    # The Java wrappers cannot be built without shared libs.
    # Fortran fails built with shared for old HDF5 versions
    conflicts("+fortran", when="+shared@:1.8.15")
    # See https://github.com/spack/spack/issues/31085
    conflicts("+fortran+mpi", when="@1.8.22")
    # See https://github.com/HDFGroup/hdf5/issues/2906#issue-1697749645

    # HDF5 searches for zlib CMake config files before it falls back to
    # FindZLIB.cmake. We don't build zlib with CMake by default, so have to
    # delete the first search, otherwise it may find a system zlib. See
    # https://github.com/HDFGroup/hdf5/issues/4904
    patch("find_package_zlib.patch", when="@1.8.16:1.14.4")

    # There are several officially unsupported combinations of the features:
    # 1. Thread safety is not guaranteed via high-level C-API but in some cases
    #    it works.
    # conflicts('+threadsafe+hl')

    # 2. Thread safety is not guaranteed via Fortran (CXX) API, but it's
    #    possible for a dependency tree to contain a package that uses Fortran
    #    (CXX) API in a single thread and another one that uses low-level C-API
    #    in multiple threads. To allow for such scenarios, we don't specify the
    #    following conflicts.
    # conflicts('+threadsafe+cxx')
    # conflicts('+threadsafe+fortran')

    # 3. Parallel features are not supported via CXX API, but for the reasons
    #    described in #2 we allow for such combination.
    # conflicts('+mpi+cxx')

    # Patch needed for HDF5 1.14.3 to fix signaling FPE checks from triggering
    # at dynamic type system initialization. The type system's builtin types
    # were refactored in 1.14.3 and switched from compile-time to run-time
    # initialization. This patch suppresses floating point exception checks
    # that would otherwise be triggered by this code. Later HDF5 versions
    # will include the patch code changes.
    # See https://github.com/HDFGroup/hdf5/pull/3837

    # There are known build failures with intel@18.0.1. This issue is
    # discussed and patch is provided at
    # https://software.intel.com/en-us/forums/intel-fortran-compiler-for-linux-and-mac-os-x/topic/747951.

    # Turn line comments into block comments to conform with pre-C99 language
    # standards. Versions of hdf5 after 1.8.10 don't require this patch,
    # either because they conform to pre-C99 or neglect to ask for pre-C99
    # language standards from their compiler. The hdf5 build system adds
    # the -ansi cflag (run 'man gcc' for info on -ansi) for some versions
    # of some compilers (see hdf5-1.8.10/config/gnu-flags). The hdf5 build
    # system does not provide an option to disable -ansi, but since the
    # pre-C99 code is restricted to just five lines of line comments in
    # three src files, this patch accomplishes the simple task of patching the
    # three src files and leaves the hdf5 build system alone.

    # There are build errors with GCC 8, see
    # https://forum.hdfgroup.org/t/1-10-2-h5detect-compile-error-gcc-8-1-0-on-centos-7-2-solved/4441

    # Disable MPI C++ interface when C++ is disabled, otherwise downstream
    # libraries fail to link; see https://github.com/spack/spack/issues/12586
    patch(
        "h5public-skip-mpicxx.patch",
        when="@1.8.10:1.8.21,1.10.0:1.10.5+mpi~cxx",
        sha256="b61e2f058964ad85be6ee5ecea10080bf79e73f83ff88d1fa4b602d00209da9c",
    )

    # Fixes BOZ literal constant error when compiled with GCC 10.
    # The issue is described here: https://github.com/spack/spack/issues/18625


    # This patch may only be needed with GCC 11.2 on macOS, but it's valid for
    # any of the head HDF5 versions as of 12/2021. Since it's impossible to
    # tell what Fortran version is part of a mixed apple-clang toolchain on
    # macOS (which is the norm), and this might be an issue for other compilers
    # as well, we just apply it to all platforms.
    # See https://github.com/HDFGroup/hdf5/issues/1157

    # Patch needed for HDF5 1.14.0 where dependency on MPI::MPI_C was declared
    # PUBLIC.  Dependent packages using the default hdf5 package but not
    # expecting to use MPI then failed to configure because they did not call
    # find_package(MPI).  This patch does that for them.  Later HDF5 versions
    # will include the patch code changes.

    # The argument 'buf_size' of the C function 'h5fget_file_image_c' is
    # declared as intent(in) though it is modified by the invocation. As a
    # result, aggressive compilers such as Fujitsu's may do a wrong
    # optimization to cause an error.
    # The parallel compiler wrappers (i.e. h5pcc, h5pfc, etc.) reference MPI
    # compiler wrappers and do not need to be changed.
    # These do not exist on Windows.
    # Enable only for supported target platforms.

    if sys.platform != "win32":
        filter_compiler_wrappers(
            "h5cc", "h5hlcc", "h5fc", "h5hlfc", "h5c++", "h5hlc++", relative_root="bin"
        )

