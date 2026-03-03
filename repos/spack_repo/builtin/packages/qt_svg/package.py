# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.packages.qt_base.package import QtBase, QtPackage

from spack.package import *


class QtSvg(QtPackage):
    """Scalable Vector Graphics (SVG) is an XML-based language for describing
    two-dimensional vector graphics. Qt provides classes for rendering and
    displaying SVG drawings in widgets and on other paint devices."""

    url = QtPackage.get_url(__qualname__)
    list_url = QtPackage.get_list_url(__qualname__)


    variant("widgets", default=False, description="Build SVG widgets.")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("qt-base +gui")
    depends_on("qt-base +widgets", when="+widgets")

    for _v in QtBase.versions:
        v = str(_v)
        depends_on("qt-base@" + v, when="@" + v)

    def cmake_args(self):
        args = super().cmake_args() + []
        return args
