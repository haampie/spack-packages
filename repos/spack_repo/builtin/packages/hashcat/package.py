# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class Hashcat(MakefilePackage):
    """hashcat is the world's fastest and most advanced password recovery
    utility, supporting five unique modes of attack for over 300 highly
    optimized hashing algorithms. hashcat currently supports CPUs, GPUs,
    and other hardware accelerators on Linux, Windows, and macOS,and has
    facilities to help enable distributed password cracking."""

    homepage = "https://hashcat.net/hashcat/"
    url = "https://github.com/hashcat/hashcat/archive/v6.1.1.tar.gz"

    license("MIT")


    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def install(self, spec, prefix):
        make("SHARED=1", "PREFIX={0}".format(prefix), "install")
