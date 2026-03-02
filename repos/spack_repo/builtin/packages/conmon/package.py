# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class Conmon(MakefilePackage):
    """An OCI container runtime monitor that tracks and logs container lifecycle events."""

    homepage = "https://github.com/containers/conmon"
    url = "https://github.com/containers/conmon/archive/v2.0.30.tar.gz"
    git = "https://github.com/containers/conmon.git"

    maintainers("bernhardkaindl")

    license("Apache-2.0")

    sanity_check_is_file = ["bin/conmon"]

    version("main", branch="main")
    version("2.1.13", sha256="350992cb2fe4a69c0caddcade67be20462b21b4078dae00750e8da1774926d60")

    depends_on("c", type="build")
    depends_on("go", type="build")
    depends_on("go-md2man", type="build")
    depends_on("pkgconfig", type="build")

    depends_on("glib")
    depends_on("libseccomp")

    def install(self, spec, prefix):
        make("install", f"PREFIX={prefix}")
