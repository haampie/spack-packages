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


    version("57.1", sha256="ff8c67cb65949b1e7808f2359f2b80f722697048e90e7cfc382ec1fe229e9581")

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


    depends_on("python", type="build", when="@64.1:")
    with when("build_system=autotools"):
        depends_on("autoconf", type="build")

    with when("build_system=msbuild platform=windows"):
        patch("ICU4C_NMAKE_NO_DOUBLE_QUOTE_VARS.patch", when="@64.1:")



    # Need to make sure that locale is UTF-8 in order to process source files in UTF-8.
class MSBuildBuilder(msbuild.MSBuildBuilder):
    # Need to make sure that locale is UTF-8 in order to process source files in UTF-8.
    @property
    def build_directory(self):
        solution_path = pathlib.Path(self.pkg.stage.source_path)
        if self.spec.satisfies("@:67"):
            solution_path = solution_path / "icu"
        solution_path = solution_path / "source" / "allinone"
        return str(solution_path)

    def install(self, pkg, spec, prefix):
        mkdirp(prefix.lib)
        mkdirp(prefix.bin)
        mkdirp(prefix.include)
        with working_dir(self.pkg.stage.source_path):
            # install bin
            install_tree("bin64", prefix.bin)
            # install lib
            install_tree("lib64", prefix.lib)
            # intstall headers
            install_tree("include", prefix.include)
