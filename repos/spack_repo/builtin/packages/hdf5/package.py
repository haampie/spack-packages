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

    license("custom")

    # The 'develop' version is renamed so that we could uninstall (or patch) it
    # without affecting other develop version.

    # Odd versions are considered experimental releases
    # Even versions are maintenance versions

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


    # The Java wrappers cannot be built without shared libs.
    # Fortran fails built with shared for old HDF5 versions
    # See https://github.com/spack/spack/issues/31085
    # See https://github.com/HDFGroup/hdf5/issues/2906#issue-1697749645

    # HDF5 searches for zlib CMake config files before it falls back to
    # FindZLIB.cmake. We don't build zlib with CMake by default, so have to
    # delete the first search, otherwise it may find a system zlib. See
    # https://github.com/HDFGroup/hdf5/issues/4904

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
    def patch(self):
        filter_file(
            "INTEGER(SIZE_T), INTENT(IN) :: buf_size",
            "INTEGER(SIZE_T), INTENT(OUT) :: buf_size",
            "fortran/src/H5Fff.F90",
            string=True,
            ignore_absent=True,
        )
        filter_file(
            "INTEGER(SIZE_T), INTENT(IN) :: buf_size",
            "INTEGER(SIZE_T), INTENT(OUT) :: buf_size",
            "fortran/src/H5Fff_F03.f90",
            string=True,
            ignore_absent=True,
        )
        if self.run_tests:
            # hdf5 has ~2200 CPU-intensive tests, some of them have races:
            # Often, these loop endless(at least on one Xeon and one EPYC).
            # testphdf5 fails indeterministic. This fixes finishing the tests
            filter_file(
                "REMOVE_ITEM H5P_TESTS",
                "REMOVE_ITEM H5P_TESTS t_bigio t_shapesame testphdf5",
                "testpar/CMakeTests.cmake",
            )

    # The parallel compiler wrappers (i.e. h5pcc, h5pfc, etc.) reference MPI
    # compiler wrappers and do not need to be changed.
    # These do not exist on Windows.
    # Enable only for supported target platforms.

    if sys.platform != "win32":
        filter_compiler_wrappers(
            "h5cc", "h5hlcc", "h5fc", "h5hlfc", "h5c++", "h5hlc++", relative_root="bin"
        )

    def url_for_version(self, version):
        url = "https://support.hdfgroup.org/archive/support/ftp/HDF5/releases/hdf5-{0}/hdf5-{1}/src/hdf5-{1}.tar.gz"
        return url.format(version.up_to(2), version)

    def flag_handler(self, name, flags):
        spec = self.spec
        cmake_flags = []

        if name == "cflags":
            if (
                spec.satisfies("%gcc")
                or spec.satisfies("%clang")
                or spec.satisfies("%apple-clang")
                or spec.satisfies("%oneapi")
            ):
                # Quiet warnings/errors about implicit declaration of functions
                # in C99:
                cmake_flags.append("-Wno-error=implicit-function-declaration")
                # Note that this flag will cause an error if building %nvhpc.
            if spec.satisfies("@:1.8.12~shared"):
                # More recent versions set CMAKE_POSITION_INDEPENDENT_CODE to
                # True and build with PIC flags.
                cmake_flags.append(self.compiler.cc_pic_flag)
            if spec.satisfies("@1.8.21 %oneapi@2023.0.0"):
                cmake_flags.append("-Wno-error=int-conversion")
        elif name == "cxxflags":
            if spec.satisfies("@:1.8.12+cxx~shared"):
                cmake_flags.append(self.compiler.cxx_pic_flag)
        elif name == "fflags":
            if spec.satisfies("+fortran%cce"):
                # Cray compiler generates module files with uppercase names by
                # default, which is not handled by the CMake scripts. The
                # following flag forces the compiler to produce module files
                # with lowercase names.
                cmake_flags.append("-ef")
            if spec.satisfies("@:1.8.12+fortran~shared"):
                cmake_flags.append(self.compiler.fc_pic_flag)
        elif name == "ldlibs":
            if spec.satisfies("+fortran %fj"):
                cmake_flags.extend(["-lfj90i", "-lfj90f", "-lfjsrcinfo", "-lelf"])

        return flags, None, (cmake_flags or None)

    @property
    def libs(self):
        """HDF5 can be queried for the following parameters:

        - "hl": high-level interface
        - "cxx": C++ APIs
        - "fortran": Fortran APIs
        - "java": Java APIs

        :return: list of matching libraries
        """
        query_parameters = self.spec.last_query.extra_parameters

        shared = self.spec.satisfies("+shared")

        # This map contains a translation from query_parameters
        # to the libraries needed
        query2libraries = {
            tuple(): ["libhdf5"],
            ("cxx", "fortran", "hl", "java"): [
                # When installed with Autotools, the basename of the real
                # library file implementing the High-level Fortran interface is
                # 'libhdf5hl_fortran'. Starting versions 1.8.22, 1.10.5 and
                # 1.12.0, the Autotools installation also produces a symbolic
                # link 'libhdf5_hl_fortran.<so/a>' to
                # 'libhdf5hl_fortran.<so/a>'. Note that in the case of the
                # dynamic library, the latter is a symlink to the real sonamed
                # file 'libhdf5_fortran.so.<abi-version>'. This means that all
                # dynamically linked executables/libraries of the dependent
                # packages need 'libhdf5_fortran.so.<abi-version>' with the same
                # DT_SONAME entry. However, the CMake installation (at least
                # starting version 1.8.10) does not produce it. Instead, the
                # basename of the library file is 'libhdf5_hl_fortran'. Which
                # means that switching to CMake requires rebuilding of all
                # dependant packages that use the High-level Fortran interface.
                # Therefore, we do not try to preserve backward compatibility
                # with Autotools installations by creating symlinks. The only
                # packages that could benefit from it would be those that
                # hardcode the library name in their building systems. Such
                # packages should simply be patched.
                "libhdf5_hl_fortran",
                "libhdf5_hl_f90cstub",
                "libhdf5_hl_cpp",
                "libhdf5_hl",
                "libhdf5_fortran",
                "libhdf5_f90cstub",
                "libhdf5_java",
                "libhdf5",
            ],
            ("cxx", "hl"): ["libhdf5_hl_cpp", "libhdf5_hl", "libhdf5"],
            ("fortran", "hl"): [
                "libhdf5_hl_fortran",
                "libhdf5_hl_f90cstub",
                "libhdf5_hl",
                "libhdf5_fortran",
                "libhdf5_f90cstub",
                "libhdf5",
            ],
            ("hl",): ["libhdf5_hl", "libhdf5"],
            ("cxx", "fortran"): ["libhdf5_fortran", "libhdf5_f90cstub", "libhdf5_cpp", "libhdf5"],
            ("cxx",): ["libhdf5_cpp", "libhdf5"],
            ("fortran",): ["libhdf5_fortran", "libhdf5_f90cstub", "libhdf5"],
            ("java",): ["libhdf5_java", "libhdf5"],
        }

        # Turn the query into the appropriate key
        key = tuple(sorted(query_parameters))
        libraries = query2libraries[key]

        return find_libraries(libraries, root=self.prefix, shared=shared, recursive=True)

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("-showconfig", output=str, error=str)
        match = re.search(r"HDF5 Version: (\d+\.\d+\.\d+)(\D*\S*)", output)
        return match.group(1) if match else None

    @classmethod
    def determine_variants(cls, exes, version):
        def is_enabled(text):
            return text.lower() in ["t", "true", "enabled", "yes", "1", "on"]

        results = []
        for exe in exes:
            variants = []
            output = Executable(exe)("-showconfig", output=str, error=os.devnull)
            match = re.search(r"High-level library: (\S+)", output)
            if match and is_enabled(match.group(1)):
                variants.append("+hl")
            else:
                variants.append("~hl")

            match = re.search(r"Parallel HDF5: (\S+)", output)
            if match and is_enabled(match.group(1)):
                variants.append("+mpi")
            else:
                variants.append("~mpi")

            match = re.search(r"C\+\+: (\S+)", output)
            if match and is_enabled(match.group(1)):
                variants.append("+cxx")
            else:
                variants.append("~cxx")

            match = re.search(r"Fortran: (\S+)", output)
            if match and is_enabled(match.group(1)):
                variants.append("+fortran")
            else:
                variants.append("~fortran")

            match = re.search(r"Java: (\S+)", output)
            if match and is_enabled(match.group(1)):
                variants.append("+java")
            else:
                variants.append("~java")

            match = re.search(r"Threadsafety: (\S+)", output)
            if match and is_enabled(match.group(1)):
                variants.append("+threadsafe")
            else:
                variants.append("~threadsafe")

            match = re.search(r"Build HDF5 Tools: (\S+)", output)
            if match and is_enabled(match.group(1)):
                variants.append("+tools")
            else:
                variants.append("~tools")

            match = re.search(r"I/O filters \(external\): \S*(szip\(encoder\))\S*", output)
            if match:
                variants.append("+szip")
            else:
                variants.append("~szip")

            match = re.search(r"Default API mapping: (\S+)", output)
            if match and match.group(1) in set(["v200", "v114", "v112", "v110", "v18", "v16"]):
                variants.append("api={0}".format(match.group(1)))

            results.append(" ".join(variants))

        return results

