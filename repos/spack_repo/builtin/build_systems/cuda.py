# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import re
from typing import Iterable, List
from spack.package import PackageBase, any_combination_of, conflicts, depends_on, variant, when
class CudaPackage(PackageBase):
    cuda_arch_values = (
        "10",
        "11",
        "12",
        "13",
        "20",
        "121f",
    )
