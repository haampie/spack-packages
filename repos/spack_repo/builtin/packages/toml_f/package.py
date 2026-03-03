# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems import cmake, meson
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.build_systems.meson import MesonPackage

from spack.package import *


class TomlF(MesonPackage, CMakePackage):
    """TOML parser implementation for data serialization and deserialization in Fortran"""

    homepage = "https://toml-f.readthedocs.io/"
    url = "https://github.com/toml-f/toml-f/releases/download/v0.4.2/toml-f-0.4.2.tar.xz"
    git = "https://github.com/toml-f/toml-f/"


    build_system("cmake", "meson", default="meson")


    depends_on("fortran", type="build")  # generated
    depends_on("meson@0.57.2:", type="build", when="build_system=meson")

    depends_on("pkgconfig", type="build")


class CMakeBuilder(cmake.CMakeBuilder):
    def cmake_args(self):
        return []


class MesonBuilder(meson.MesonBuilder):
    def meson_args(self):
        return []
