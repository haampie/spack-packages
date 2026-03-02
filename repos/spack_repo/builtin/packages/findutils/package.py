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

    def url_for_version(self, version):
        # Before 4.7.0 it used tar.gz instead of tar.xz
        if version < Version("4.7.0"):
            self.gnu_mirror_path = "findutils/findutils-{0}.tar.gz".format(version)

        return super().url_for_version(version)

    executables = ["^find$"]


    version("4.2.26", sha256="74fa9030b97e074cbeb4f6c8ec964c5e8292cf5a62b195086113417f75ab836a")
    version("4.2.25", sha256="a2bc59e80ee599368584f4ac4a6e647011700e1b5230e65eb3170c603047bb51")


    depends_on("gettext@0.19.8:", type="build")

    depends_on("faketime", when="@4.5.13:", type="test")

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
