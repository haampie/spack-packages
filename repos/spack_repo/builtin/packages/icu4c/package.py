# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pathlib
from spack_repo.builtin.build_systems import autotools, msbuild
from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.msbuild import MSBuildPackage
from spack.package import *
class Icu4c(AutotoolsPackage, MSBuildPackage):
    """ICU is a mature, widely used set of C/C++ and Java libraries providing
    Unicode and Globalization support for software applications. ICU4C is the
    C/C++ interface."""
    homepage = "http://site.icu-project.org/"
    url = "https://github.com/unicode-org/icu/releases/download/release-65-1/icu4c-65_1-src.tgz"
    build_system("autotools", "msbuild", default="autotools")
    for plat in ["linux", "darwin", "freebsd"]:
        with when(f"platform={plat}"):
            variant(
                "cxxstd",
                default="17",
                values=(conditional("11", "14", when="@:74"), "17"),
                multi=False,
                description="Use the specified C++ standard when building",
            )
    with when("build_system=autotools"):
        depends_on("automake", type="build")
        depends_on("libtool", type="build")
