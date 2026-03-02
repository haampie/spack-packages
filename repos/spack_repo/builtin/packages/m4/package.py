# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import re
from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.gnu import GNUMirrorPackage
from spack.package import *
class M4(AutotoolsPackage, GNUMirrorPackage):
    """GNU M4 is an implementation of the traditional Unix macro processor."""
    homepage = "https://www.gnu.org/software/m4/m4.html"
    gnu_mirror_path = "m4/m4-1.4.18.tar.gz"
    version("1.4.21", sha256="38ae59f7a30bf9c108193cc5c25fbb06014f21e230c7ede2eff614f7b7c37ed8")
    version("1.4.20", sha256="6ac4fc31ce440debe63987c2ebbf9d7b6634e67a7c3279257dc7361de8bdb3ef")
    # The NVIDIA compilers do not currently support some GNU builtins.
    # Detect this case and use the fallback path.
    # Workaround bug where __LONG_WIDTH__ is not defined
    # from: https://github.com/Homebrew/homebrew-core/blob/master/Formula/m4.rb
    # Patch credit to Jeremy Huddleston Sequoia <jeremyhu@apple.com>
    # from: https://www.mail-archive.com/m4-patches@gnu.org/msg01208.html
    # tests: Fix failing test checks/198.sysval with upstream patch for doc/m4.texi
    depends_on("c", type="build")  # generated
    # Older versions require too many patches for newer compilers
    with when("@:1.4.18"):
        conflicts("%gcc@14:", msg="This version is incompatible with gcc@14:")
    # Fix c++17 '[[nodiscard]]' attribute ordering (fixed in 1.4.20)
    build_directory = "spack-build"
    tags = ["build-tools"]
    executables = ["^g?m4$"]
