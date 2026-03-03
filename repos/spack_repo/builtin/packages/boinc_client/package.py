# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class BoincClient(AutotoolsPackage):
    """BOINC is a platform for high-throughput computing on a
    large scale (thousands or millions of computers). It can be
    used for volunteer computing (using consumer devices) or
    grid computing (using organizational resources). It
    supports virtualized, parallel, and GPU-based
    applications."""

    homepage = "https://boinc.berkeley.edu/"
    url = "https://github.com/BOINC/boinc/archive/client_release/7.16/7.16.5.tar.gz"

    license("LGPL-3.0-only")

    version("7.16.5", sha256="33db60991b253e717c6124cce4750ae7729eaab4e54ec718b9e37f87012d668a")

    variant("manager", default=False, description="Builds the client manager")
    variant("graphics", default=False, description="Graphic apps support")

    # Dependency documentation:
    # https://boinc.berkeley.edu/trac/wiki/SoftwarePrereqsUnix
    conflicts("%gcc@:3.0.4")





    depends_on("sqlite@3.1:", when="+manager")

    patch("systemd-fix.patch")

    def configure_args(self):
        spec = self.spec
        args = []

        args.append("--disable-server")
        args.append("--enable-client")

        if spec.satisfies("+manager"):
            args.append("--enable-manager")
        else:
            args.append("--disable-manager")

        return args
