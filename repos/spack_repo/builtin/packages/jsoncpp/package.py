# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems import cmake, meson
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.build_systems.meson import MesonPackage

from spack.package import *


class Jsoncpp(CMakePackage, MesonPackage):
    """JsonCpp is a C++ library that allows manipulating JSON values,
    including serialization and deserialization to and from strings.
    It can also preserve existing comment in unserialization/serialization
    steps, making it a convenient format to store user input files."""

    homepage = "https://github.com/open-source-parsers/jsoncpp"
    url = "https://github.com/open-source-parsers/jsoncpp/archive/1.7.3.tar.gz"
    tags = ["windows"]


    version("1.8.4", sha256="c49deac9e0933bcb7044f08516861a2d560988540b23de2ac1ad443b219afdb6")
    version("1.7.7", sha256="087640ebcf7fbcfe8e2717a0b9528fff89c52fcf69fa2a18cc2b538008098f97")
    version("1.7.6", sha256="07cf5d4f184394ec0a9aa657dd4c13ea682c52a1ab4da2fb176cb2d5501101e8")
    version("1.7.5", sha256="4338c6cab8af8dee6cdfd54e6218bd0533785f552c6162bb083f8dd28bf8fbbe")
    version("1.7.4", sha256="10dcd0677e80727e572a1e462193e51a5fde3e023b99e144b2ee1a469835f769")
    version("1.7.3", sha256="1cfcad14054039ba97c22531888796cb9369e6353f257aacaad34fda956ada53")

    # From 1.9.3 onwards CMAKE_CXX_STANDARD is finally set to 11.
    variant(
        "cxxstd",
        default="default",
        values=("default", conditional("98", when="@:1.8"), "11", "14", "17"),
        multi=False,
        description="Use the specified C++ standard when building.",
        when="@:1.9.2 build_system=cmake",
    )

    build_system("cmake", conditional("meson", when="@1.9.2:"), default="cmake")

    depends_on("cxx", type="build")  # generated

    with when("build_system=cmake"):
        depends_on("cmake@3.1:", type="build")
        depends_on("cmake@3.9:", when="@1.9:", type="build")

    with when("build_system=meson"):
        depends_on("meson@0.49.0:", type="build")
        depends_on("meson@0.56.0:", type="build", when="@1.9.6:")

    depends_on("python", type="test")

    # Ref: https://github.com/open-source-parsers/jsoncpp/pull/1023
    # Released in 1.9.2, patch does not apply cleanly across releases.
    # May apply to more compilers in the future.
    @when("@:1.9.1 %clang@10.0.0:")
    def patch(self):
        filter_file(
            "return d >= min && d <= max;",
            "return d >= static_cast<double>(min) && d <= static_cast<double>(max);",
            "src/lib_json/json_value.cpp",
        )


class CMakeBuilder(cmake.CMakeBuilder):
    def cmake_args(self):
        args = [
            self.define("BUILD_SHARED_LIBS", True),
            self.define("JSONCPP_WITH_TESTS", self.pkg.run_tests),
        ]
        if "cxxstd" in self.spec.variants:
            cxxstd = self.spec.variants["cxxstd"].value
            if cxxstd != "default":
                args.append(self.define("CMAKE_CXX_STANDARD", cxxstd))
        return args


class MesonBuilder(meson.MesonBuilder):
    def meson_args(self):
        return ["-Dtests={}".format("true" if self.pkg.run_tests else "false")]
