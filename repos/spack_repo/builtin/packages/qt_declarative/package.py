# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.packages.qt_base.package import QtBase, QtPackage

from spack.package import *


class QtDeclarative(QtPackage):
    """Qt Declarative (Quick 2)."""

    url = QtPackage.get_url(__qualname__)
    list_url = QtPackage.get_list_url(__qualname__)


    depends_on("c", type="build")
    depends_on("cxx", type="build")

    # Testing requires +network
    depends_on("qt-base +network", type="test")

    for _v in QtBase.versions:
        v = str(_v)
        depends_on("qt-base@" + v, when="@" + v)
        depends_on("qt-shadertools@" + v, when="@" + v)
