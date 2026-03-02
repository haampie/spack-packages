# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class BashCompletion(AutotoolsPackage):
    """Programmable completion functions for bash."""

    homepage = "https://github.com/scop/bash-completion"
    url = "https://github.com/scop/bash-completion/archive/2.3.tar.gz"
    git = "https://github.com/scop/bash-completion.git"


    version("2.3", sha256="d92fcef5f6e3bbc68a84f0a7b063a1cd07b4000cc6e275cd1ff83863ab3b322a")

    depends_on("c", type="build")  # generated

    # Build dependencies
    depends_on("automake", type="build")
    depends_on("autoconf", type="build")
    depends_on("libtool", type="build")

    # Other dependencies
    depends_on("bash@4.1:", type="run")

    @run_before("install")
    def create_install_directory(self):
        mkdirp(join_path(self.prefix.share, "bash-completion", "completions"))

    @run_after("install")
    def show_message_to_user(self):
        prefix = self.prefix
        # Guidelines for individual user as provided by the author at
        # https://github.com/scop/bash-completion
        print("=====================================================")
        print("Bash completion has been installed. To use it, please")
        print("include the following lines in your ~/.bash_profile :")
        print("")
        print("# Use bash-completion, if available")
        print(f"[[ $PS1 && -f {prefix}/share/bash-completion/bash_completion ]] && \\")
        print(f"    . {prefix}/share/bash-completion/bash_completion")
        print("")
        print("=====================================================")
