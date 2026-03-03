# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Simdjson(CMakePackage):
    """simdjson is a SIMD-accelerated JSON parsing library for C++ that can parse gigabytes of JSON
    text per second."""

    homepage = "https://simdjson.org"
    url = "https://github.com/simdjson/simdjson/archive/v3.12.2.tar.gz"



    depends_on("c", type="build")
    depends_on("cxx", type="build")

    # variants by library linkage type
    variant("shared", default=False, description="Build a dynamically linked library")
    variant(
        "simdjson_static",
        default=False,
        description="Build the simdjson_static library along with the dynamically linked simdjson",
        when="+shared",
    )

    # feature variants
    variant("exceptions", default=True, description="Enable exception throwing")
    variant("threads", default=True, description="Enable multithreading")
    variant("deprecated", default=True, description="Enable deprecated APIs")
    variant("utf8-validation", default=True, description="Enable UTF-8 validation")

    # variants for enabling sanitizers
    variant("ubsan", default=False, description="Enable UndefinedBehaviorSanitizer")
    variant("tsan", default=False, description="Enable ThreadSanitizer", when="+ubsan")
    variant("asan", default=False, description="Enable AddressSanitizer")
    variant("msan", default=False, description="Enable MemorySanitizer")

    conflicts("+asan+msan", msg="AddressSanitizer and MemorySanitizer cannot be combined")
    conflicts("+asan+tsan", msg="AddressSanitizer and ThreadSanitizer cannot be combined")
    conflicts("+msan+tsan", msg="MemorySanitizer and ThreadSanitizer cannot be combined")

    # https://clang.llvm.org/docs/MemorySanitizer.html#supported-platforms
    requires(
        "platform=linux %clang",
        "platform=freebsd %clang",
        when="+msan",
        msg="MemorySanitizer is supported only by Clang and on Linux, FreeBSD, and NetBSD",
    )

    def cmake_args(self):
        build_type = self.spec.variants["build_type"]
        enable_dev_checks = "Debug" in build_type or "RelWithDebInfo" in build_type

        return [
            "-DSIMDJSON_DEVELOPER_MODE:BOOL=OFF",
            "-DSIMDJSON_VERBOSE_LOGGING:BOOL=OFF",
            self.define("SIMDJSON_DEVELOPMENT_CHECKS", enable_dev_checks),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("SIMDJSON_BUILD_STATIC_LIB", "simdjson_static"),
            self.define_from_variant("SIMDJSON_ENABLE_THREADS", "threads"),
            self.define_from_variant("SIMDJSON_EXCEPTIONS", "exceptions"),
            self.define("SIMDJSON_DISABLE_DEPRECATED_API", self.spec.satisfies("~deprecated")),
            self.define("SIMDJSON_SKIPUTF8VALIDATION", self.spec.satisfies("~utf8-validation")),
            self.define_from_variant("SIMDJSON_SANITIZE_UNDEFINED", "ubsan"),
            self.define_from_variant("SIMDJSON_SANITIZE_THREADS", "tsan"),
            self.define_from_variant("SIMDJSON_SANITIZE", "asan"),
            self.define_from_variant("SIMDJSON_SANITIZE_MEMORY", "msan"),
        ]
