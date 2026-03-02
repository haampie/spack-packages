# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.maven import MavenPackage

from spack.package import *


class Zipkin(MavenPackage):
    """Zipkin is a distributed tracing system. It helps gather timing
    data needed to troubleshoot latency problems in service
    architectures. Features include both the collection and lookup
    of this data."""

    homepage = "https://zipkin.io/"
    url = "https://github.com/openzipkin/zipkin/archive/2.21.5.tar.gz"

    license("Apache-2.0")

    version("2.21.5", sha256="e643a810f82f9ea50e2cb6847694c7645507d3deae77685a3a1bb841e0f885a2")

