from spack_repo.builtin.packages.qt_base.package import QtBase, QtPackage
from spack.package import *
class QtTools(QtPackage):
    variant(
        "assistant",
        default=False,
    )
    depends_on("c")
    depends_on("cxx")
