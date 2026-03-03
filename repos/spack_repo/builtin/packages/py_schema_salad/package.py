# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PySchemaSalad(PythonPackage):
    """Schema Annotations for Linked Avro Data (SALAD)"""

    homepage = "https://github.com/common-workflow-language/schema_salad"
    pypi = "schema-salad/schema_salad-8.7.20241021092521.tar.gz"

    license("Apache-2.0")
    version(
        "8.8.20250205075315",
        sha256="444a45509fb048347e0ec205b2af6390f0bb145f7183716ba6af2f75a22b8bdd",
    )
    version(
        "8.7.20241021092521",
        sha256="287b27adff70e55dd715bfbea18bb1a58fd73de14b4273be4038559308089cdf",
    )
    version(
        "8.3.20221209165047",
        sha256="d97cc9a4d7c4255eb8000bcebaa8ac0d1d31801c921fd4113ab3051c1e326c7c",
    )



    def url_for_version(self, version):
        url = (
            "https://files.pythonhosted.org/packages/source/s/schema-salad/schema{}salad-{}.tar.gz"
        )
        if version >= Version("8.5.20240503091721"):
            sep = "_"
        else:
            sep = "-"
        return url.format(sep, version)
