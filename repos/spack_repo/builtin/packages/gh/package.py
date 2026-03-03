# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.go import GoPackage

from spack.package import *


class Gh(GoPackage):
    """GitHub's official command line tool."""

    homepage = "https://github.com/cli/cli"
    url = "https://github.com/cli/cli/archive/refs/tags/v2.0.0.tar.gz"



    conflicts("platform=darwin", when="@2.28.0")

    depends_on("go@1.24:", type="build", when="@2.74.2:")
    depends_on("go@1.23:", type="build", when="@2.66:")
    depends_on("go@1.22.5:", type="build", when="@2.56:")
    depends_on("go@1.22:", type="build", when="@2.47:")
    depends_on("go@1.21:", type="build", when="@2.33:")
    depends_on("go@1.19:", type="build", when="@2.21:")
    depends_on("go@1.18:", type="build", when="@2.10:")
    depends_on("go@1.16:", type="build")

    @property
    def build_args(self):
        args = super().build_args
        args.extend(["-trimpath", "./cmd/gh"])
        return args

    @property
    def check_args(self):
        args = super().check_args
        skip_tests = (
            "TestHasNoActiveToken|TestTokenStoredIn.*|"
            "TestSwitchUser.*|TestSwitchClears.*|"
            "TestTokenWorksRightAfterMigration|"
            "Test_loginRun.*|Test_logoutRun.*|Test_refreshRun.*|"
            "Test_setupGitRun.*|Test_CheckAuth|TestSwitchRun.*|"
            "Test_statusRun.*|TestTokenRun.*"
        )
        args.extend([f"-skip={skip_tests}", "./..."])
        return args

    @run_after("install")
    def install_completions(self):
        gh = Executable(self.prefix.bin.gh)

        mkdirp(bash_completion_path(self.prefix))
        with open(bash_completion_path(self.prefix) / "gh", "w") as file:
            gh("completion", "-s", "bash", output=file)

        mkdirp(fish_completion_path(self.prefix))
        with open(fish_completion_path(self.prefix) / "gh.fish", "w") as file:
            gh("completion", "-s", "fish", output=file)

        mkdirp(zsh_completion_path(self.prefix))
        with open(zsh_completion_path(self.prefix) / "_gh", "w") as file:
            gh("completion", "-s", "zsh", output=file)
