# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class NfCoreTools(PythonPackage):
    """A python package with helper tools for the nf-core community."""

    homepage = "https://nf-co.re/tools"
    pypi = "nf-core/nf-core-2.7.1.tar.gz"
    maintainers("marcodelapierre")

    license("MIT")

    version("2.7.2", sha256="585be3908b9b93ee9263b99dd779818d48d51f6e7f44a42aa79e626617e7af48")
    version("2.7.1", sha256="90de62390314ef3141cee700667f017aa65c0346e40704a0f70d0662abcfb0db")
    version("2.6", sha256="47d4df906a60006249284bbf0bb84cdec48303a699c7c0d0a26f404a50e0811a")
    version("2.5.1", sha256="0303f6e3810ba1bc6ac843566ee9dea6b5edbf3527437dec5854b8c437456a4f")



