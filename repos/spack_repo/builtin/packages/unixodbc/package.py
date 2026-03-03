# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Unixodbc(AutotoolsPackage):
    """ODBC is an open specification for providing application developers with
    a predictable API with which to access Data Sources. Data Sources include
    SQL Servers and any Data Source with an ODBC Driver."""

    homepage = "https://www.unixodbc.org/"
    url = "https://www.unixodbc.org/unixODBC-2.3.4.tar.gz"


    depends_on("c", type="build")

    depends_on("iconv")

    @property
    def libs(self):
        return find_libraries("libodbc", root=self.prefix, recursive=True)
