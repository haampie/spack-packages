# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin.packages.qt_base.package import QtBase, QtPackage
from spack.package import *
class QtTools(QtPackage):
    """Qt Tools contains tools like Qt Designer."""
    url = QtPackage.get_url(__qualname__)
    git = QtPackage.get_git(__qualname__)
    list_url = QtPackage.get_list_url(__qualname__)
    # src/assistant/qlitehtml is a submodule that is not in the git archive
    variant(
        "assistant",
        default=False,
        description="Qt Assistant for viewing on-line documentation in Qt help file format.",
    )
    variant(
        "designer",
        default=False,
        description="Qt Widgets Designer for designing and building GUIs with Qt Widgets.",
    )
    # use of relative path in https://github.com/qt/qttools/blob/6.8.2/.gitmodules
    conflicts("+assistant", when="@6.8.2", msg="Incorrect git submodule prevents +assistant")
    depends_on("c")
    depends_on("cxx")
    for _v in QtBase.versions:
        v = str(_v)
    def cmake_args(self):
        return super().cmake_args() + [
            self.define_qt_feature("fullqthelp", True),
        ]
