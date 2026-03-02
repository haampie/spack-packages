# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import sys
from pathlib import Path
from spack_repo.builtin.build_systems.generic import Package
from spack.package import *
class Boost(Package):
    git = "https://github.com/boostorg/boost.git"
    list_url = "https://sourceforge.net/projects/boost/files/boost/"
