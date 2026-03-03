# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Strace(AutotoolsPackage):
    """Strace is a diagnostic, debugging and instructional userspace
    utility for Linux. It is used to monitor and tamper with interactions
    between processes and the Linux kernel, which include system calls,
    signal deliveries, and changes of process state."""

    homepage = "https://strace.io"
    url = "https://github.com/strace/strace/releases/download/v6.11/strace-6.11.tar.xz"



    variant("mpers", default=False, description="Enable multiple personalities support")

    depends_on("c", type="build")
    depends_on("gawk", when="+mpers", type="build")

    conflicts("platform=darwin", msg="strace runs only on Linux")
    conflicts("platform=windows", msg="strace runs only on Linux")

    def configure_args(self):
        args = []
        if self.spec.satisfies("+mpers"):
            args.append("--enable-mpers=yes")
        else:
            args.append("--enable-mpers=no")
        return args
