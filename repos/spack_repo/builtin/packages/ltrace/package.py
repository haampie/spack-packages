# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Ltrace(AutotoolsPackage):
    """Ltrace intercepts and records dynamic library calls which are called
    by an executed process and the signals received by that process. It
    can also intercept and print the system calls executed by the program."""

    homepage = "https://www.ltrace.org"
    url = "https://www.ltrace.org/ltrace_0.7.3.orig.tar.bz2"





    depends_on("elf", type="link")

    def configure_args(self):
        # Disable -Werror since some functions used by ltrace
        # have been deprecated in recent version of glibc
        return ["--disable-werror"]
