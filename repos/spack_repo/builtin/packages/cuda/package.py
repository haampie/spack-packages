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
            "4c7ac59d1f41d67be27d140a4622801738ad71088570a0facfd6ec878a4c4100",
            "https://developer.download.nvidia.com/compute/cuda/13.0.1/local_installers/cuda_13.0.1_580.82.07_linux.run",
        ),
    },
    "13.0.0": {
        "Linux-aarch64": (
            "d956c956d0aef7270f26e6d8a9dbb2aeb3bd0d2214195c0e0e230a4cd37ff3d2",
            "https://developer.download.nvidia.com/compute/cuda/13.0.0/local_installers/cuda_13.0.0_580.65.06_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "c64969f35ad99bf3f9e8acb8e3d22355150c6ca07acc16a853778600a9b65ba6",
            "https://developer.download.nvidia.com/compute/cuda/13.0.0/local_installers/cuda_13.0.0_580.65.06_linux.run",
        ),
    },
    "12.9.1": {
        "Linux-aarch64": (
            "64f47ab791a76b6889702425e0755385f5fa216c5a9f061875c7deed5f08cdb6",
            "https://developer.download.nvidia.com/compute/cuda/12.9.1/local_installers/cuda_12.9.1_575.57.08_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "0f6d806ddd87230d2adbe8a6006a9d20144fdbda9de2d6acc677daa5d036417a",
            "https://developer.download.nvidia.com/compute/cuda/12.9.1/local_installers/cuda_12.9.1_575.57.08_linux.run",
        ),
    },
    "12.9.0": {
        "Linux-aarch64": (
            "f3b7ae71f95d11de0a03ccfa1c0aff7be336d2199b50b1a15b03695fd15a6409",
            "https://developer.download.nvidia.com/compute/cuda/12.9.0/local_installers/cuda_12.9.0_575.51.03_linux_sbsa.run",
            "991e436c7a6c94ec67cf44204d136adfef87baa3ded270544fa211179779bc40",
            "https://developer.download.nvidia.com/compute/cuda/6_0/rel/installers/cuda_6.0.37_linux_64.run",
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
    executables = ["^nvcc$"]
    skip_version_audit = ["platform=darwin", "platform=windows"]
    for ver, packages in _versions.items():
        pkg = packages.get(f"{platform.system()}-{platform.machine()}")
        if pkg:
            version(ver, sha256=pkg[0], url=pkg[1], expand=False)
