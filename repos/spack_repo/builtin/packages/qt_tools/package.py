from spack_repo.builtin.packages.qt_base.package import QtBase, QtPackage
from spack.package import *
class QtTools(QtPackage):
    variant(
        "assistant",
        default=False,
        description="Qt Assistant for viewing on-line documentation in Qt help file format.",
    )
    # use of relative path in https://github.com/qt/qttools/blob/6.8.2/.gitmodules
    conflicts("+assistant", when="@6.8.2", msg="Incorrect git submodule prevents +assistant")
    depends_on("c")
    depends_on("cxx")
