# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack_repo.builtin.build_systems import autotools, cmake
from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class ZlibNg(AutotoolsPackage, CMakePackage):
    """zlib replacement with optimizations for next generation systems."""

    homepage = "https://github.com/zlib-ng/zlib-ng"
    url = "https://github.com/zlib-ng/zlib-ng/archive/2.0.0.tar.gz"
    git = "https://github.com/zlib-ng/zlib-ng.git"

    maintainers("haampie")

    license("Zlib")


    variant("compat", default=True, description="Enable compatibility API")


    variant("new_strategies", default=True, description="Enable new deflate strategies")

    provides("zlib-api", when="+compat")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # Default to autotools, since cmake would result in circular dependencies if it's not
    # reused.
    build_system("autotools", "cmake", default="autotools")

    # fix building with NVHPC, see https://github.com/zlib-ng/zlib-ng/pull/1698
    patch("pr-1698.patch", when="@2.1.4:2.1.6+opt%nvhpc")

    with when("build_system=cmake"):
        depends_on("cmake@3.5.1:", type="build")
        depends_on("cmake@3.14.0:", type="build", when="@2.1.0:")


    @property
    def libs(self):
        compat_name = "zlib" if sys.platform == "win32" else "libz"
        non_compat_name = "zlib-ng" if sys.platform == "win32" else "libz-ng"
        name = compat_name if self.spec.satisfies("+compat") else non_compat_name
        return find_libraries(
            name,
            root=self.prefix,
            recursive=True,
            shared=self.spec.satisfies("+shared"),
            runtime=False,
        )

    def flag_handler(self, name, flags):
        if name == "cflags" and self.spec.satisfies("+pic build_system=autotools"):
            flags.append(self["c"].pic_flag)
        return (flags, None, None)


class AutotoolsBuilder(autotools.AutotoolsBuilder):
    @run_before("configure")
    def pretend_gcc(self):
        # All nice things (PIC flags, symbol versioning) that happen to the compilers that are
        # recognized as gcc (%gcc, %clang, %intel, %oneapi) we want for some other compilers too:
            self.define_from_variant("WITH_OPTIM", "opt"),
