from spack.package import (
    EnvironmentModifications,
    PackageBase,
)
class ROCmPackage(PackageBase):
    """Auxiliary class which contains ROCm variant, dependencies and conflicts
    """
    # https://llvm.org/docs/AMDGPUUsage.html
