#            c: /opt/rocm/llvm/bin/clang++
#            cxx: /opt/rocm/llvm/bin/clang++
#      buildable: false
#
#    It is advisable to replace /rocm/ in the paths above with /rocm-version/
#    and introduce spec version numbers to ensure reproducible results.
#
# 3. In part 2, DO NOT list the path to hsa as /opt/rocm/hsa ! You want spack
#    to find hsa in /opt/rocm/include/hsa/hsa.h . The directory of
#    /opt/rocm/hsa also has an hsa.h file, but it won't be found because spack
#    does not like its directory structure.
#
import os
from spack.package import (
    EnvironmentModifications,
    PackageBase,
    any_combination_of,
    conflicts,
    depends_on,
    variant,
)
class ROCmPackage(PackageBase):
    """Auxiliary class which contains ROCm variant, dependencies and conflicts
    and is meant to unify and facilitate its usage. Closely mimics CudaPackage.
    Maintainers: dtaller
    """
    # https://llvm.org/docs/AMDGPUUsage.html
    # Possible architectures
    amdgpu_targets = (
        "gfx701",
        "gfx801",
        "gfx802",
        "gfx803",
        "gfx900",
        "gfx900:xnack-",
        "gfx902",
        "gfx1251",
    )
    variant("rocm", default=False, description="Enable ROCm support")
    # possible amd gpu targets for rocm builds
