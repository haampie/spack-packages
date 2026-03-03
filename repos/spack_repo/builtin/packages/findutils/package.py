# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.gnu import GNUMirrorPackage

from spack.package import *


class Findutils(AutotoolsPackage, GNUMirrorPackage):
    """The GNU Find Utilities are the basic directory searching
    utilities of the GNU operating system."""

    tags = ["core-packages"]

    homepage = "https://www.gnu.org/software/findutils/"
    gnu_mirror_path = "findutils/findutils-4.8.0.tar.xz"

    executables = ["^find$"]

    version("4.10.0", sha256="1387e0b67ff247d2abde998f90dfbf70c1491391a59ddfecb8ae698789f0a4f5")
    version("4.9.0", sha256="a2bfb8c09d436770edc59f50fa483e785b161a3b7b9d547573cb08065fd462fe")
    version("4.8.0", sha256="57127b7e97d91282c6ace556378d5455a9509898297e46e10443016ea1387164")
    version("4.7.0", sha256="c5fefbdf9858f7e4feb86f036e1247a54c79fc2d8e4b7064d5aaa1f47dfa789a")
    version("4.6.0", sha256="ded4c9f73731cd48fec3b6bdaccce896473b6d8e337e9612e16cf1431bb1169d")
    version("4.4.2", sha256="434f32d171cbc0a5e72cfc5372c6fc4cb0e681f8dce566a0de5b6fccd702b62a")
    version("4.4.1", sha256="77a5b85d7fe0dd9c1093e010b61f765707364ec2c89c4f432c1c616215bcc138")




    # The NVIDIA compilers do not currently support some GNU builtins.
    # Detect this case and use the fallback path.
    # Workaround bug where __LONG_WIDTH__ is not defined
    # Auto-detecting whether `__attribute__((__nonnull__(...)))` is supported
    # does not work for GCC on macOS
    # <https://savannah.gnu.org/bugs/?func=detailitem&item_id=59972>; we thus
    # disable this attribute manually

    build_directory = "spack-build"

    # Taken from here to build 4.8.0 with apple-clang:
    # https://github.com/Homebrew/homebrew-core/blob/master/Formula/findutils.rb
    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        if self.spec.satisfies("@4.8.0 %apple-clang"):
            env.set("CFLAGS", "-D__nonnull\\(params\\)=")

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"find \(GNU findutils\)\s+(\S+)", output)
        return match.group(1) if match else None
