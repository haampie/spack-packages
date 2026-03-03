# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cargo import CargoPackage

from spack.package import *


class KakouneLsp(CargoPackage):
    """Kakoune Language Server Protocol Client"""

    homepage = "https://github.com/kakoune-lsp/kakoune-lsp"
    url = "https://github.com/kakoune-lsp/kakoune-lsp/archive/refs/tags/v17.0.1.tar.gz"



