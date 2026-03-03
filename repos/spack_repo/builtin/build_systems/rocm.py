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
    )
    # need amd gpu type for rocm builds
    # https://github.com/ROCm-Developer-Tools/HIP/blob/master/bin/hipcc
