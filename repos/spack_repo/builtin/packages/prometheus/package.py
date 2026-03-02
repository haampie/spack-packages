# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class Prometheus(MakefilePackage):
    """Prometheus, a Cloud Native Computing Foundation project, is a
    systems and service monitoring system."""

    homepage = "https://prometheus.io/"
    url = "https://github.com/prometheus/prometheus/archive/refs/tags/v2.55.1.tar.gz"

    license("Apache-2.0")

    version("2.17.1", sha256="443590c1896cf5096b75d4a30e45381c84a5d17712dc714109ea8cf418b275ac")
    version("2.17.0", sha256="c94b13677003838d795c082b95878903d43cd21ab148996d39f1900f00370c97")

    depends_on("c", type="build")  # generated

    depends_on("go@1.17:", type="build", when="@2.37.0:")
    depends_on("go@1.16:", type="build", when="@2.33.0:")
    depends_on("go@1.14:", type="build", when="@2.23.0:")
    depends_on("go@1.13:", type="build", when="@2.17.0:")

    depends_on("node-js@16:", type="build", when="@2.31.0:")
    depends_on("node-js@11.10.1:", type="build")

    depends_on("npm@7:", type="build", when="@2.31.0:")
    depends_on("npm", type="build", when="@2.30.0:")
    depends_on("yarn@1", type="build", when="@:2.29.2")

    def build(self, spec, prefix):
        make("build", parallel=False)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("prometheus", prefix.bin)
        install("promtool", prefix.bin)
        if spec.satisfies("@:2.19.2"):
            install("tsdb/tsdb", prefix.bin)
        install_tree("documentation", prefix.documentation)
