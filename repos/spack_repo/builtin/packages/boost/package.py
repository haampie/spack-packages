# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import sys
from pathlib import Path
from spack_repo.builtin.build_systems.generic import Package
from spack.package import *
class Boost(Package):
    """Boost provides free peer-reviewed portable C++ source
    libraries, emphasizing libraries that work well with the C++
    Standard Library.
    Boost libraries are intended to be widely useful, and usable
    across a broad spectrum of applications. The Boost license
    encourages both commercial and non-commercial use.
    """
    homepage = "https://www.boost.org"
    url = "https://downloads.sourceforge.net/project/boost/boost/1.55.0/boost_1_55_0.tar.bz2"
    git = "https://github.com/boostorg/boost.git"
    list_url = "https://sourceforge.net/projects/boost/files/boost/"
    list_depth = 1
    with_default_variants = "boost" + "".join(
        [
            "+atomic",
            "+serialization",
            "+system",
            "+test",
            "+thread",
            "+timer",
            "+wave",
        ]
    )
    # mpi/python are not installed by default because they pull in many
    # dependencies and/or because there is a great deal of customization
    # possible (and it would be difficult to choose sensible defaults)
    #
    # Boost.Container can be both header-only and compiled. '+container'
    # indicates the compiled version which requires Extended Allocator
