# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.packages.qt_base.package import QtBase, QtPackage

from spack.package import *


class QtQuick3d(QtPackage):
    """A new module and API for defining 3D content in Qt Quick."""

    url = QtPackage.get_url(__qualname__)
    list_url = QtPackage.get_list_url(__qualname__)


    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("qt-base +network", when="@6.3.0:")

    depends_on("assimp@5.0.1:")
    depends_on("embree", when="@6.4:")

    vendor_deps_to_remove = ["assimp", "embree"]

    for _v in QtBase.versions:
        v = str(_v)
        depends_on("qt-base@" + v, when="@" + v)
        depends_on("qt-declarative@" + v, when="@" + v)
        depends_on("qt-quicktimeline@" + v, when="@" + v)

    def cmake_args(self):
        args = super().cmake_args() + [
            self.define("FEATURE_quick3d_assimp", True),
            self.define("FEATURE_system_assimp", True),
        ]
        return args
