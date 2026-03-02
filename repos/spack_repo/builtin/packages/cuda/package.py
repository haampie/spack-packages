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
        ),
        "Linux-x86_64": (
            "023e571fe26ee829c98138dfc305a92279854aac7d184d255fd58c06c6af3c17",
            "https://developer.download.nvidia.com/compute/cuda/11.1.1/local_installers/cuda_11.1.1_455.32.00_linux_ppc64le.run",
        ),
    },
    "11.1.0": {
        "Linux-aarch64": (
            "878cbd36c5897468ef28f02da50b2f546af0434a8a89d1c724a4d2013d6aa993",
            "https://developer.download.nvidia.com/compute/cuda/11.1.0/local_installers/cuda_11.1.0_455.23.05_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "858cbab091fde94556a249b9580fadff55a46eafbcb4d4a741d2dcd358ab94a5",
            "https://developer.download.nvidia.com/compute/cuda/11.1.0/local_installers/cuda_11.1.0_455.23.05_linux.run",
        ),
        "Linux-x86_64": (
            "e7c22dc21278eb1b82f34a60ad7640b41ad3943d929bebda3008b72536855d31",
            "https://developer.download.nvidia.com/compute/cuda/10.1/Prod/local_installers/cuda_10.1.243_418.87.00_linux.run",
        ),
        "Linux-ppc64le": (
            "b198002eef010bab9e745ae98e47567c955d00cf34cc8f8d2f0a6feb810523bf",
            "https://developer.download.nvidia.com/compute/cuda/10.1/Prod/local_installers/cuda_10.1.243_418.87.00_linux_ppc64le.run",
        ),
    },
    "10.0.130": {
        "Linux-x86_64": (
            "92351f0e4346694d0fcb4ea1539856c9eb82060c25654463bfd8574ec35ee39a",
            "https://developer.nvidia.com/compute/cuda/10.0/Prod/local_installers/cuda_10.0.130_410.48_linux",
        )
    },
    "9.2.88": {
        "Linux-x86_64": (
            "8d02cc2a82f35b456d447df463148ac4cc823891be8820948109ad6186f2667c",
            "https://developer.nvidia.com/compute/cuda/9.2/Prod/local_installers/cuda_9.2.88_396.26_linux",
        )
    },
    "9.1.85": {
        "Linux-x86_64": (
            "8496c72b16fee61889f9281449b5d633d0b358b46579175c275d85c9205fe953",
            "https://developer.nvidia.com/compute/cuda/9.1/Prod/local_installers/cuda_9.1.85_387.26_linux",
        )
    },
    "9.0.176": {
        "Linux-x86_64": (
            "96863423feaa50b5c1c5e1b9ec537ef7ba77576a3986652351ae43e66bcd080c",
            "https://developer.nvidia.com/compute/cuda/9.0/Prod/local_installers/cuda_9.0.176_384.81_linux-run",
        )
    },
    "8.0.61": {
        "Linux-x86_64": (
            "9ceca9c2397f841024e03410bfd6eabfd72b384256fbed1c1e4834b5b0ce9dc4",
            "https://developer.nvidia.com/compute/cuda/8.0/Prod2/local_installers/cuda_8.0.61_375.26_linux-run",
        )
    },
    "8.0.44": {
        "Linux-x86_64": (
            "64dc4ab867261a0d690735c46d7cc9fc60d989da0d69dc04d1714e409cacbdf0",
            "https://developer.nvidia.com/compute/cuda/8.0/prod/local_installers/cuda_8.0.44_linux-run",
        )
    },
    "7.5.18": {
        "Linux-x86_64": (
            "08411d536741075131a1858a68615b8b73c51988e616e83b835e4632eea75eec",
            "https://developer.download.nvidia.com/compute/cuda/7.5/Prod/local_installers/cuda_7.5.18_linux.run",
        )
    },
    "6.5.14": {
        "Linux-x86_64": (
            "f3e527f34f317314fe8fcd8c85f10560729069298c0f73105ba89225db69da48",
            "https://developer.download.nvidia.com/compute/cuda/6_5/rel/installers/cuda_6.5.14_linux_64.run",
        )
    },
    "6.0.37": {
        "Linux-x86_64": (
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
        "allow-unsupported-compilers",
        default=False,
        sticky=True,
        description="Allow unsupported host compiler and CUDA version combinations",
    )
    # cuda-gdb needed libncurses.so.5 before 11.4.0
    # see https://docs.nvidia.com/cuda/archive/11.3.1/cuda-gdb/index.html#common-issues-oss
    # see https://docs.nvidia.com/cuda/archive/11.4.0/cuda-gdb/index.html#release-notes
    # Avoid binding stub libraries by absolute path
    non_bindable_shared_objects = ["stubs"]
    # contains precompiled binaries without rpaths
    unresolved_libraries = ["*"]
