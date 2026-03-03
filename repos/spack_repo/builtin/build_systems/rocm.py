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
        "gfx904",
        "gfx906",
        "gfx906:xnack-",
        "gfx908",
        "gfx908:xnack-",
        "gfx909",
        "gfx90a",
        "gfx90a:xnack-",
        "gfx90a:xnack+",
        "gfx90c",
        "gfx940",
        "gfx941",
        "gfx942",
        "gfx950",
        "gfx1010",
        "gfx1011",
        "gfx1012",
        "gfx1013",
        "gfx1030",
        "gfx1031",
        "gfx1032",
        "gfx1033",
        "gfx1034",
        "gfx1035",
        "gfx1036",
        "gfx1100",
        "gfx1101",
        "gfx1102",
        "gfx1103",
        "gfx1150",
        "gfx1151",
        "gfx1152",
        "gfx1153",
        "gfx1200",
        "gfx1201",
        "gfx1250",
        "gfx1251",
    )
    variant("rocm", default=False, description="Enable ROCm support")
    # possible amd gpu targets for rocm builds
    variant(
        "amdgpu_target",
        description="AMD GPU architecture",
        values=any_combination_of(*amdgpu_targets),
        sticky=True,
        when="+rocm",
    )
    # need amd gpu type for rocm builds
    # https://github.com/ROCm-Developer-Tools/HIP/blob/master/bin/hipcc
    # It seems that hip-clang does not (yet?) accept this flag, in which case
    # we will still need to set the HCC_AMDGPU_TARGET environment flag in the
    # hip package file. But I will leave this here for future development.
    # HIP version vs Architecture
    # TODO: add a bunch of lines like:
    # depends_on('hip@:6.0', when='amdgpu_target=gfx701')
    # to indicate minimum version for each architecture.
    # Add compiler minimum versions based on the first release where the
    # processor is included in llvm/lib/Support/TargetParser.cpp
    # Compiler conflicts
    # TODO: add conflicts statements along the lines of
    # arch_platform = ' target=x86_64: platform=linux'
    # conflicts('%gcc@5:', when='+cuda ^cuda@:7.5' + arch_platform)
    # conflicts('platform=darwin', when='+cuda ^cuda@11.0.2:')
    # for hip-related limitations.
