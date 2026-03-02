# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.packages.boost.package import Boost

from spack.package import *

yaml_cpp_tests_libcxx_error_msg = "yaml-cpp tests incompatible with libc++"


class YamlCpp(CMakePackage):
    """A YAML parser and emitter in C++"""

    homepage = "https://github.com/jbeder/yaml-cpp"
    url = "https://github.com/jbeder/yaml-cpp/archive/0.8.0.tar.gz"
    git = "https://github.com/jbeder/yaml-cpp.git"
    maintainers("eschnett")

    license("MIT")

    version("develop", branch="master")

    variant("tests", default=False, description="Build yaml-cpp tests using internal gtest")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("boost@:1.66", when="@0.5.0:0.5.3")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, when="@0.5.0:0.5.3")

    # Explicitly include <cstdint>
    # See https://github.com/jbeder/yaml-cpp/pull/1310


    def flag_handler(self, name, flags):
        # We cannot catch all conflicts with the conflicts directive because
        # the user can add arbitrary strings to the flags. Here we can at least
        # fail early.
        # We'll include cppflags in case users mistakenly put c++ flags there.
        if (
            name in ("cxxflags", "cppflags")
            and self.spec.satisfies("+tests")
            and "-stdlib=libc++" in flags
        ):
            raise InstallError(yaml_cpp_tests_libcxx_error_msg)
        return (flags, None, None)

    def cmake_args(self):
        options = []

        options.extend(
            [
                self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
                self.define_from_variant("YAML_BUILD_SHARED_LIBS", "shared"),
                self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"),
                self.define_from_variant("YAML_CPP_BUILD_TESTS", "tests"),
            ]
        )

        return options

    def url_for_version(self, version):
        url = "https://github.com/jbeder/yaml-cpp/archive/{0}.tar.gz"
        if version < Version("0.5.3"):
            return url.format(f"release-{version}")
        elif version < Version("0.8.0"):
            return url.format(f"yaml-cpp-{version}")
        else:
            return url.format(version)
