# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import re
from typing import Iterable, List
from spack.package import PackageBase, any_combination_of, conflicts, depends_on, variant, when
class CudaPackage(PackageBase):
    """Auxiliary class which contains CUDA variant, dependencies and conflicts
    and is meant to unify and facilitate its usage.
    Maintainers: ax3l, Rombur, davidbeckingsale, pauleonix
    """
    # https://docs.nvidia.com/cuda/cuda-compiler-driver-nvcc/index.html#gpu-feature-list
    # https://developer.nvidia.com/cuda-gpus
    # https://en.wikipedia.org/wiki/CUDA#GPUs_supported
    cuda_arch_values = (
        "10",
        "11",
        "12",
        "13",
        "20",
        "21",
        "30",
        "32",
        "35",
        "37",
        "50",
        "52",
        "53",
        "121",
        "121a",
        "121f",
    )
    # FIXME: keep cuda and cuda_arch separate to make usage easier until
    # Spack has depends_on(cuda, when='cuda_arch!=None') or alike
    # Maxwell support:
    # Pascal support:
    # Volta support:
    # Turing support:
    # Ampere support:
    # Ada support:
    # Hopper support:
