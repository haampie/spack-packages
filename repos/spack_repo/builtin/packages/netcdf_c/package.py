# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import itertools
import os
import sys

from spack_repo.builtin.build_systems import autotools, cmake
from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class NetcdfC(CMakePackage, AutotoolsPackage):
    """NetCDF (network Common Data Form) is a set of software libraries and
    machine-independent data formats that support the creation, access, and
    sharing of array-oriented scientific data. This is the C distribution."""

    homepage = "https://www.unidata.ucar.edu/software/netcdf"
    git = "https://github.com/Unidata/netcdf-c.git"
    url = "https://github.com/Unidata/netcdf-c/archive/refs/tags/v4.8.1.tar.gz"



    version("4.8.0", sha256="aff58f02b1c3e91dc68f989746f652fe51ff39e6270764e484920cb8db5ad092")
    # Version 4.4.1.1 is having problems in tests
    #    https://github.com/Unidata/netcdf-c/issues/343
    # Version 4.4.1 can crash on you (in real life and in tests).  See:
    #    https://github.com/Unidata/netcdf-c/issues/282
    version("4.4.1", sha256="17599385fd76ccdced368f448f654de2ed000fece44dece9fb5d598798b4c9d6")

    with when("build_system=cmake"):
        # TODO: document why we need to revert https://github.com/Unidata/netcdf-c/pull/1731
        #  with the following patch:

        # TODO: https://github.com/Unidata/netcdf-c/pull/2595 contains some of the changes
        # made in this patch but is not sufficent to replace the patch. There is currently
        # no upstream PR (or set of PRs) covering all changes in this path.
        # When #2595 lands, this patch should be updated to include only
        # the changes not incorporated into that PR

        # Building netcdf-c w/ hdf5+mpi causes CMake's FindMPI to inject a path to the current
        # netcdf-c source directory into its targets interface properties causing CMake configure
        # failures. This patch strips the source dir from the MPI include interface

        # Netcdf's source for the h5deflate target contains includes for zlib headers
        # but fails to include that header in the include interface in the relevant
        # CMake target, this patch adds that.
        # Similar to https://github.com/Unidata/netcdf-c/pull/3132

        # Netcdf-c, on Windows, attempts to glob from the CMake prefix path
        # which is wrong for a multidue of development and CMake practices reasons
        # is error prone because it uses Windows paths (and prevents installation)
        # and has no relation to actual runtime requirements for netcdf-c
        # Additionally, Spack on Windows already does this for every package
        # so remove this behavior from netcdf-c
        patch("netcdf-c-4.7-9.2_no_glob_deps.patch", when="@4.7:4.9.2 platform=windows")

    # Some of the patches touch configure.ac and, therefore, require forcing the autoreconf stage:
    _force_autoreconf_when = []
    with when("build_system=autotools"):
        # See https://github.com/Unidata/netcdf-c/pull/1752

        # See https://github.com/Unidata/netcdf-c/pull/2293
        _force_autoreconf_when.append("@4.8.1")

        # See https://github.com/Unidata/netcdf-c/pull/2710
        # Versions 4.9.0 and 4.9.1 had a bug in the configure script, which worked to our benefit.
        # The bug has been fixed in
        # https://github.com/Unidata/netcdf-c/commit/267b26f1239310ca7ba8304315834939f7cc9886 and
        # now we need a patch in cases when we build for macOS with DAP disabled:
        patch(
            "https://github.com/Unidata/netcdf-c/commit/cfe6231aa6b018062b443cbe2fd9073f15283344.patch?full_index=1",
            sha256="4e105472de95a1bb5d8b0b910d6935ce9152777d4fe18b678b58347fa0122abc",
            when="@4.9.2~dap platform=darwin",
        )
        _force_autoreconf_when.append("@4.9.2~dap platform=darwin")

    with when("@4.7.2"):
        # Fix headers
        # See https://github.com/Unidata/netcdf-c/pull/1505
        patch(
            "https://github.com/Unidata/netcdf-c/commit/cca9ae64f622bb2b7f164fa352c820b5fe4d132c.patch?full_index=1",
            sha256="495b3e5beb7f074625bcec2ca76aebd339e42719e9c5ccbedbdcc4ffb81a7450",
        )
        # See https://github.com/Unidata/netcdf-c/pull/1508
        patch(
            "https://github.com/Unidata/netcdf-c/commit/f0dc61a73c8a35432034c8d262f1893a0090c3ed.patch?full_index=1",
            sha256="19e7f31b96536928621b1c29bb6d1a57bcb7aa672cea8719acf9ac934cdd2a3e",
        )

    # See https://github.com/Unidata/netcdf-c/pull/2618
    patch(
        "https://github.com/Unidata/netcdf-c/commit/00a722b253bae186bba403d0f92ff1eba719591f.patch?full_index=1",
        sha256="25b83de1e081f020efa9e21c94c595220849f78c125ad43d8015631d453dfcb9",
        when="@4.9.0:4.9.1~mpi+parallel-netcdf",
    )

    # See https://github.com/Unidata/netcdf-c/issues/2674
    patch(
        "https://github.com/Unidata/netcdf-c/commit/f8904d5a1d89420dde0f9d2c0e051ba08d08e086.patch?full_index=1",
        sha256="0161eb870fdfaf61be9d70132c9447a537320342366362e76b8460c823bf95ca",
        when="@4.9.0:4.9.2",
    )

    variant("mpi", default=True, description="Enable parallel I/O for netcdf-4")
    variant("parallel-netcdf", default=False, description="Enable parallel I/O for classic files")
    variant("hdf4", default=False, description="Enable HDF4 support")
    variant("pic", default=True, description="Produce position-independent code (for shared libs)")
    variant("shared", default=True, description="Enable shared library")
    variant("dap", default=False, description="Enable DAP support")
    variant("byterange", default=False, description="Enable byte-range I/O")
    variant("jna", default=False, description="Enable JNA support")
    variant("fsync", default=False, description="Enable fsync support")
    variant("nczarr_zip", default=False, description="Enable NCZarr zipfile format storage")
    variant("optimize", default=True, description="Enable -O2 for a more optimized lib")
    variant("logging", default=False, description="Enable logging")

    variant("szip", default=True, description="Enable Szip compression plugin")
    variant("blosc", default=True, description="Enable Blosc compression plugin")
    variant("zstd", default=True, description="Enable Zstandard compression plugin")


    with when("build_system=cmake"):
        # Based on the versions required by the root CMakeLists.txt:
        depends_on("cmake@2.8.12:", type="build", when="@4.3.3:4.3")
        depends_on("cmake@2.8.11:", type="build", when="@4.4.0:")
        # Starting version 4.9.1, nczarr_test/CMakeLists.txt relies on the FILE_PERMISSIONS feature
        # of the configure_file command, which is only available starting CMake 3.20:

    with when("build_system=autotools"):
        for __s in itertools.chain(["@main"], _force_autoreconf_when):
            with when(__s):
                depends_on("automake", type="build")
                depends_on("libtool", type="build")
                depends_on("m4", type="build")
        del __s

    # M4 is also needed for the source and man file generation. All the generated source files are
    # included in the release tarballs starting at least the oldest supported version:
    depends_on("m4", type="build", when="@main")

    # The man files are included in the release tarballs starting version 4.5.0 but they are not
    # needed for the Windows platform:
    for __p in ["darwin", "linux"]:
        with when("platform={0}".format(__p)):
            # It is possible to install the package with CMake and without M4 on a non-Windows
            # platform but some of the man files will not be installed in that case (even if they
            # are in the release tarball):
            depends_on("m4", type="build", when="build_system=cmake")
            # Apart from the redundant configure-time check, which we suppress below, M4 is not
            # needed when building with Autotools if the man files are in the release tarball:
    del __p


    # curl 7.18.0 or later is required:
    # https://docs.unidata.ucar.edu/nug/current/getting_and_building_netcdf.html

    # curl is supposed to only be needed when +dap or +byterange, but the check is missing
    # this is fixed in 4.9.3. Spack autotools already protects against this
    # https://github.com/Unidata/netcdf-c/issues/3016
    depends_on("curl@7.18.0:", when="@:4.9.2 build_system=cmake")

    # Need to include libxml2 when using DAP in 4.9.0 and newer to build
    # https://github.com/Unidata/netcdf-c/commit/53464e89635a43b812b5fec5f7abb6ff34b9be63

    depends_on("parallel-netcdf", when="+parallel-netcdf")

    # parallel I/O features is enabled:
    depends_on("mpi", when="+mpi")
    depends_on("mpi", when="+parallel-netcdf")

    # We also need to use MPI wrappers when building against static MPI-enabled HDF5:

    # High-level API of HDF5 1.8.9 or later is required for netCDF-4 support:
    # https://docs.unidata.ucar.edu/nug/current/getting_and_building_netcdf.html
    # Starting version 4.4.0, it became possible to disable parallel I/O even
    # if HDF5 supports it. For previous versions of the library we need
    # HDF5 without mpi support to disable parallel I/O:

    # We need HDF5 with mpi support to enable parallel I/O.

    # NetCDF 4.4.0 and prior have compatibility issues with HDF5 1.10 and later
    # https://github.com/Unidata/netcdf-c/issues/250

    # NetCDF 4.7.4 and prior require HDF5 1.10 or older
    # https://github.com/Unidata/netcdf-c/pull/1671

    # Although NetCDF 4.8.0 builds and passes the respective tests against HDF5 1.12.0 with the
    # default API (i.e. the problem reported in https://github.com/Unidata/netcdf-c/issues/1965 is
    # not reproducible), the configure script fails if HDF5 1.12.0 is built without api=v18
    # (according to the error message emitted by the configure script) or api=v110 (according to
    # the comments in the configure script and its implementation). The check that led to the
    # failure was removed in version 4.8.1 (https://github.com/Unidata/netcdf-c/pull/2044). To
    # keep it simple, we require HDF5 1.10.x or older:

    with when("+byterange"):
        # HDF5 implements H5allocate_memory starting version 1.8.15:
        # HDF5 defines H5FD_FEAT_DEFAULT_VFD_COMPATIBLE (required when version 1.10.x is used)
        # starting version 1.10.2:
        depends_on("hdf5@:1.9,1.10.2:")
        # The macro usage was adjusted (required when versions 1.8.23+, 1.10.8+, 1.12.1+ and
        # 1.13.0+ of HDF5 are used) in NetCDF 4.8.1
        # (see https://github.com/Unidata/netcdf-c/pull/2034):
        # Compatibility with HDF5 1.14.x was introduced in NetCDF 4.9.2
        # (see https://github.com/Unidata/netcdf-c/pull/2615):
        depends_on("hdf5@:1.12", when="@:4.9.1")

    depends_on("libzip", when="+nczarr_zip")

    # According to the documentation (see
    # https://docs.unidata.ucar.edu/nug/current/getting_and_building_netcdf.html), zlib 1.2.5 or
    # later is required for netCDF-4 compression. However, zlib became a direct dependency only
    # starting NetCDF 4.9.0 (for the deflate plugin):
    depends_on("zlib-api", when="@4.9.0:+shared")
    depends_on("zlib@1.2.5:", when="^[virtuals=zlib-api] zlib")

    # Use the vendored bzip2 on Windows:
    for __p in ["darwin", "linux"]:
        depends_on("bzip2", when="@4.9.0:+shared platform={0}".format(__p))
    del __p


    # Byte-range I/O was added in version 4.7.0:

    # Byte-range requires DAP starting version 4.9.3:
    requires("+dap", when="@4.9.3:+byterange")

    # JNA was added in 4.3.2 and removed in 4.9.3:

    # NCZarr was added in version 4.8.0 as an experimental feature and became a supported one in
    # version 4.8.1:

    # The features were introduced in version 4.9.0:
    with when("@:4.8"):

        conflicts("+zstd")

    default_build_system = "cmake" if sys.platform == "win32" else "autotools"

    build_system("cmake", "autotools", default=default_build_system)

    def setup_run_environment(self, env: EnvironmentModifications) -> None:
        if self.spec.satisfies("@4.9.0:+shared"):
            # Both HDF5 and NCZarr backends honor the same environment variable:
            env.append_path("HDF5_PLUGIN_PATH", self.prefix.plugins)
        # Some packages, e.g. ncview, refuse to build if the compiler path returned by nc-config
    def cmake_args(self):
        # In 4.9.3, all CMake options were prefixed.
        # Ref. https://github.com/Unidata/netcdf-c/pull/2895
        nc = "NETCDF_" if self.spec.satisfies("@4.9.3:") else ""

        # h5_test fails when run in parallel
        make("check", parallel=False)
