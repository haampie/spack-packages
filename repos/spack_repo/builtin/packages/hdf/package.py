# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Hdf(AutotoolsPackage):
    """HDF4 (also known as HDF) is a library and multi-object
    file format for storing and managing data between machines."""

    homepage = "https://portal.hdfgroup.org"
    url = "https://support.hdfgroup.org/ftp/HDF/releases/HDF4.2.14/src/hdf-4.2.14.tar.gz"
    list_url = "https://support.hdfgroup.org/ftp/HDF/releases/"
    list_depth = 2
    maintainers("lrknox")


    variant("szip", default=False, description="Enable szip support")
    variant(
        "external-xdr", default=sys.platform != "darwin", description="Use an external XDR backend"
    )
    variant("netcdf", default=False, description="Build NetCDF API (version 2.3.2)")
    variant("fortran", default=False, description="Enable Fortran interface")
    variant("java", default=False, description="Enable Java JNI interface")
    variant("shared", default=False, description="Enable shared library")
    variant("pic", default=True, description="Produce position-independent code")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("zlib-api")
    depends_on("jpeg")

    depends_on("java@7:", when="+java", type=("build", "run"))
    # https://forum.hdfgroup.org/t/cant-build-hdf-4-2-14-with-jdk-11-and-enable-java/5702
    patch("disable_doclint.patch", when="@:4.2.14^java@9:")
    conflicts("^libjpeg@:6a")
    # configure: error: Cannot build shared fortran libraries.
    # Please configure with --disable-fortran flag.
    conflicts("+fortran", when="+shared")
    # configure: error: Java requires shared libraries to be built
    conflicts("+java", when="~shared")

    # configure: WARNING: unrecognized options: --enable-java
    conflicts("+java", when="@:4.2.11")

    # The Java interface library uses netcdf-related macro definitions even
    # when netcdf is disabled and the macros are not defined, e.g.:
    # hdfsdsImp.c:158:30: error: 'MAX_NC_NAME' undeclared
    conflicts("+java", when="@4.2.12:4.2.13~netcdf")

    # TODO: '@:4.2.14 ~external-xdr' and the fact that we compile for 64 bit
    #  architecture should be in conflict

    # https://github.com/knedlsepp/nixpkgs/commit/c1a2918c849a5bc766c6d55d96bc6cf85c9d27f4
    patch(
        "https://src.fedoraproject.org/rpms/hdf/raw/edbe5f49646b609f5bc9aeeee5a2be47e9556e8c/f/hdf-ppc.patch?full_index=1",
        sha256="5434f29a87856aa05124c7a9409b3ec3106c30b1ad722720773623190f6bfda8",
        when="@4.2.15:",
    )
    patch(
        "https://src.fedoraproject.org/rpms/hdf/raw/edbe5f49646b609f5bc9aeeee5a2be47e9556e8c/f/hdf-4.2.4-sparc.patch?full_index=1",
        sha256="ce75518cccbeb80ab976b299225ea6104c3eec1ec13c09e2289913279fcf1b39",
        when="@4.2.15:",
    )
    patch(
        "https://src.fedoraproject.org/rpms/hdf/raw/edbe5f49646b609f5bc9aeeee5a2be47e9556e8c/f/hdf-s390.patch?full_index=1",
        sha256="f7d67e8c3d0dad8bfca308936c6ac917cc0b63222c6339a29efdce14e8be6475",
        when="@4.2.15:",
    )
    patch(
        "https://src.fedoraproject.org/rpms/hdf/raw/edbe5f49646b609f5bc9aeeee5a2be47e9556e8c/f/hdf-arm.patch?full_index=1",
        sha256="d54592df281c92e7e655b8312d18bef9ed096848de9430510e0699e98246ccd3",
        when="@4.2.15:",
    )
    patch(
        "https://src.fedoraproject.org/rpms/hdf/raw/edbe5f49646b609f5bc9aeeee5a2be47e9556e8c/f/hdf-aarch64.patch?full_index=1",
        sha256="49733dd6143be7b30a28d386701df64a72507974274f7e4c0a9e74205510ea72",
        when="@4.2.15:",
    )
    # https://github.com/jcsda/spack-stack/issues/317
    patch("hdfi_h_apple_m1.patch", when="@4.2.15: target=aarch64: platform=darwin")

    # Otherwise, we randomly get:
    # SDgetfilename:
    #   incorrect file being opened - expected <file755>, retrieved <file754>
    extra_install_tests = join_path("hdf", "util", "testfiles")

    # Filter h4cc compiler wrapper to substitute the Spack compiler
    # wrappers with the path of the underlying compilers.

    def test_ncgen_version(self):
        """ensure ncgen version matches spec"""
        self._check_version_match("ncgen")

    def test_gif_converters(self):
        """test image conversion sequence and diff"""
        base_name = "storm110"
        storm_fn = join_path(self.cached_tests_work_dir, f"{base_name}.hdf")
        if not os.path.exists(storm_fn):
            raise SkipTest(f"Missing test image {storm_fn}")

        if not os.path.exists(self.prefix.bin.hdf2gif) or not os.path.exists(
            self.prefix.bin.gif2hdf
        ):
            raise SkipTest("Missing one or more installed: 'hdf2gif', 'gif2hdf'")

        gif_fn = f"{base_name}.gif"
        new_hdf_fn = f"{base_name}gif.hdf"

        with test_part(
            self, "test_gif_converters_hdf2gif", purpose=f"convert {base_name} hdf-to-gif"
        ):
            hdf2gif = which(self.prefix.bin.hdf2gif)
            hdf2gif(storm_fn, gif_fn)

        with test_part(
            self, "test_gif_converters_gif2hdf", purpose=f"convert {base_name} gif-to-hdf"
        ):
            gif2hdf = which(self.prefix.bin.gif2hdf)
            gif2hdf(gif_fn, new_hdf_fn)

        with test_part(
            self, "test_gif_converters_hdiff", purpose=f"compare new and orig {base_name} hdf"
        ):
            hdiff = which(self.prefix.bin.hdiff)
            hdiff(new_hdf_fn, storm_fn)

    def test_list(self):
        """compare low-level HDF file information to expected"""
        base_name = "storm110"
        if not os.path.isfile(self.prefix.bin.hdfls):
            raise SkipTest("hdfls is not installed")

        test_data_dir = self.test_suite.current_test_data_dir
        details_file = os.path.join(test_data_dir, f"{base_name}.out")
        expected = get_escaped_text_output(details_file)

        storm_fn = os.path.join(self.cached_tests_work_dir, f"{base_name}.hdf")

        hdfls = which(self.prefix.bin.hdfls)
        out = hdfls(storm_fn, output=str.split, error=str.split)
        check_outputs(expected, out)
