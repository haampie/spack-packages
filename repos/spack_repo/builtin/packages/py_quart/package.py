# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyQuart(PythonPackage):
    """A Python ASGI web microframework with the same API as
    Flask."""

    homepage = "https://gitlab.com/pgjones/quart/"
    pypi = "quart/quart-0.16.3.tar.gz"

    license("MIT")

    version("0.19.8", sha256="ef567d0be7677c99890d5c6ff30e679699fe7e5fca1a90fa3b6974edd8421794")
    version("0.16.3", sha256="16521d8cf062461b158433d820fff509f98fb997ae6c28740eda061d9cba7d5e")


    # Historical dependencies

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/source/q/quart/{}-{}.tar.gz"
        if self.spec.satisfies("@:0.18.3"):
            name = "Quart"
        else:
            name = "quart"
        return url.format(name, version)
