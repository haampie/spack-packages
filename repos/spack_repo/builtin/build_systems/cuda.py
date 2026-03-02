from typing import Iterable, List
from spack.package import PackageBase, any_combination_of, conflicts, depends_on, variant, when
class CudaPackage(PackageBase):
    """Auxiliary class which contains CUDA variant, dependencies and conflicts
    """
    # https://docs.nvidia.com/cuda/cuda-compiler-driver-nvcc/index.html#gpu-feature-list
