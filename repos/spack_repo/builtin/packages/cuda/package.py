# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import platform
import re
from glob import glob
from spack_repo.builtin.build_systems.generic import Package
from spack.package import *
# FIXME Remove hack for polymorphic versions
# This package uses a ugly hack to be able to dispatch, given the same
# version, to different binary packages based on the platform that is
# running spack. See #13827 for context.
# If you need to add a new version, please be aware that:
#  - versions in the following dict are automatically added to the package
#  - version tuple must be in the form (checksum, url)
#  - checksum must be sha256
#  - package key must be in the form '{os}-{arch}' where 'os' is in the
#    format returned by platform.system() and 'arch' by platform.machine()
_versions = {
    "13.1.1": {
        "Linux-aarch64": (
            "8adcd5d4b3e1e70f7420959b97514c0c97ec729da248d54902174c4d229bfd2c",
            "https://developer.download.nvidia.com/compute/cuda/13.1.1/local_installers/cuda_13.1.1_590.48.01_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "24ff323723722781436804b392a48f691cb40de9808095d3e2192d0db6dfb8e4",
            "https://developer.download.nvidia.com/compute/cuda/13.1.1/local_installers/cuda_13.1.1_590.48.01_linux.run",
        ),
    },
    "13.1.0": {
        "Linux-aarch64": (
            "06cda49a7031b1c99f784237be5c852619379cbba9555036045044b9ddc99240",
        )
    },
}
class Cuda(Package):
    """CUDA is a parallel computing platform and programming model invented
    by NVIDIA. It enables dramatic increases in computing performance by
    harnessing the power of the graphics processing unit (GPU).
    Note: This package does not currently install the drivers necessary
    to run CUDA. These will need to be installed manually. See:
    https://docs.nvidia.com/cuda/ for details."""
    homepage = "https://developer.nvidia.com/cuda-zone"
    skip_version_audit = ["platform=darwin", "platform=windows"]
