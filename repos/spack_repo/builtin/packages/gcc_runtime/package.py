# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os
import re

from spack_repo.builtin.build_systems.generic import Package

from spack.package import *


class GccRuntime(Package):
    """Package for GCC compiler runtime libraries"""

    homepage = "https://gcc.gnu.org"
    has_code = False

    tags = ["runtime"]

    # gcc-runtime versions are declared dynamically
    skip_version_audit = ["platform=linux", "platform=darwin", "platform=windows"]


    LIBRARIES = [
        "asan",
        "atomic",
        "gcc_s",
        "gfortran",
        "gomp",
        "hwasan",
        "itm",
        "lsan",
        "quadmath",
        "ssp",
        "stdc++",
        "tsan",
        "ubsan",
    ]

    # libgfortran ABI
    provides("fortran-rt", "libgfortran")
    provides("libgfortran@3", when="@:6")
    provides("libgfortran@4", when="@7")
    provides("libgfortran@5", when="@8:")



