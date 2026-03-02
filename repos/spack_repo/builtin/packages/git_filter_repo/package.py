# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.generic import Package

from spack.package import *


class GitFilterRepo(Package):
    """Quickly rewrite Git repository history (filter-branch replacement)"""

    homepage = "https://github.com/newren/git-filter-repo"
    url = "https://github.com/newren/git-filter-repo/releases/download/v2.34.0/git-filter-repo-2.34.0.tar.xz"

    maintainers("aphedges")

    license("MIT")


    depends_on("python@3.6:", when="@2.47:", type="run")
    depends_on("python@3.5:", type="run")

    def install(self, spec, prefix):
        new_shebang = "#!{0}\n".format(self.spec["python"].command)
        filter_file("^#!/usr/bin/env python3?$", new_shebang, "git-filter-repo")
        mkdirp(prefix.bin)
        install("git-filter-repo", prefix.bin)

        mkdirp(prefix.share.man.man1)
        install("Documentation/man1/git-filter-repo.1", prefix.share.man.man1)
