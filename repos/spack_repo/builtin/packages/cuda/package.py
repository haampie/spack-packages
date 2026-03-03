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
            "https://developer.download.nvidia.com/compute/cuda/13.1.0/local_installers/cuda_13.1.0_590.44.01_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "6b4fdf2694b3d7afbc526f26412b4cf4f050b202324455053307310f53b323a7",
            "https://developer.download.nvidia.com/compute/cuda/13.1.0/local_installers/cuda_13.1.0_590.44.01_linux.run",
        ),
    },
    "13.0.2": {
        "Linux-aarch64": (
            "93ab4c77ae2bc0f1f600ef48ccd3ff25a3203a6a6161a84511a33cbf5b5621fc",
            "https://developer.download.nvidia.com/compute/cuda/13.0.2/local_installers/cuda_13.0.2_580.95.05_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "81a5d0d0870ba2022efb0a531dcc60adbdc2bbff7b3ef19d6fd6d8105406c775",
            "https://developer.download.nvidia.com/compute/cuda/13.0.2/local_installers/cuda_13.0.2_580.95.05_linux.run",
        ),
    },
    "13.0.1": {
        "Linux-aarch64": (
            "927e2c2a6a3e0d12e7e93df10dad6d8f3c688b9e27e9d2034f82d437ec2d2666",
            "https://developer.download.nvidia.com/compute/cuda/13.0.1/local_installers/cuda_13.0.1_580.82.07_linux_sbsa.run",
        ),
        "Linux-x86_64": (
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
    # macOS Mojave drops NVIDIA graphics card support -- official NVIDIA
    # drivers do not exist for Mojave. See
    # https://devtalk.nvidia.com/default/topic/1043070/announcements/faq-about-macos-10-14-mojave-nvidia-drivers/
    # Note that a CUDA Toolkit installer does exist for macOS Mojave at
    # https://developer.nvidia.com/compute/cuda/10.1/Prod1/local_installers/cuda_10.1.168_mac.dmg,
    # but support for Mojave is dropped in later versions, and none of the
    # macOS NVIDIA drivers at
    # https://www.nvidia.com/en-us/drivers/cuda/mac-driver-archive/ mention
    # Mojave support -- only macOS High Sierra 10.13 is supported.
    # cuda-12.8 libcusolver.so requires log2f@GLIBC_2.27
    variant(
        "dev", default=False, description="Enable development dependencies, i.e to use cuda-gdb"
    )
    variant(
        "allow-unsupported-compilers",
        default=False,
        sticky=True,
        description="Allow unsupported host compiler and CUDA version combinations",
    )
    # cuda-gdb needed libncurses.so.5 before 11.4.0
    # see https://docs.nvidia.com/cuda/archive/11.3.1/cuda-gdb/index.html#common-issues-oss
    # see https://docs.nvidia.com/cuda/archive/11.4.0/cuda-gdb/index.html#release-notes
