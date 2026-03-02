# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyTextualPlotext(PythonPackage):
    """A Textual widget wrapper library for Plotext"""

    homepage = "https://github.com/Textualize/textual-plotext"
    pypi = "textual-plotext/textual_plotext-1.0.1.tar.gz"


    depends_on("python@3.8:3")
    depends_on("py-poetry-core")
    depends_on("py-textual@5:")
    depends_on("py-plotext@5.2.8:5")
    depends_on("py-platformdirs")
