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
        ),
        "Linux-x86_64": (
            "bbce2b760fe2096ca1c86f729e03bf377c1519add7b2755ecc4e9b0a9e07ee43",
            "https://developer.download.nvidia.com/compute/cuda/12.9.0/local_installers/cuda_12.9.0_575.51.03_linux.run",
        ),
    },
    "12.8.1": {
        "Linux-aarch64": (
            "353cbab1b57282a1001071796efd95c1e40ec27a3375e854d12637eaa1c6107c",
            "https://developer.download.nvidia.com/compute/cuda/12.8.1/local_installers/cuda_12.8.1_570.124.06_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "228f6bcaf5b7618d032939f431914fc92d0e5ed39ebe37098a24502f26a19797",
            "https://developer.download.nvidia.com/compute/cuda/12.8.1/local_installers/cuda_12.8.1_570.124.06_linux.run",
        ),
    },
    "12.8.0": {
        "Linux-aarch64": (
            "5bc211f00c4f544da6e3fc3a549b3eb0a7e038439f5f3de71caa688f2f6b132c",
            "https://developer.download.nvidia.com/compute/cuda/12.8.0/local_installers/cuda_12.8.0_570.86.10_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "610867dcd6d94c4e36c4924f1d01b9db28ec08164e8af6c764f21b84200695f8",
            "https://developer.download.nvidia.com/compute/cuda/12.8.0/local_installers/cuda_12.8.0_570.86.10_linux.run",
        ),
    },
    "12.6.3": {
        "Linux-aarch64": (
            "213ea63a6357020978a8b0a79a8c9d12a2a5941afa1cdc69d5a3f933fa8bed04",
            "https://developer.download.nvidia.com/compute/cuda/12.6.3/local_installers/cuda_12.6.3_560.35.05_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "81d60e48044796d7883aa8a049afe6501b843f2c45639b3703b2378de30d55d3",
            "https://developer.download.nvidia.com/compute/cuda/12.6.3/local_installers/cuda_12.6.3_560.35.05_linux.run",
        ),
    },
    "12.6.2": {
        "Linux-aarch64": (
            "2249408848b705c18b9eadfb5161b52e4e36fcc5753647329cce93db141e5466",
            "https://developer.download.nvidia.com/compute/cuda/12.6.2/local_installers/cuda_12.6.2_560.35.03_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "3729a89cb58f7ca6a46719cff110d6292aec7577585a8d71340f0dbac54fb237",
            "https://developer.download.nvidia.com/compute/cuda/12.6.2/local_installers/cuda_12.6.2_560.35.03_linux.run",
        ),
    },
    "12.6.1": {
        "Linux-aarch64": (
            "b39ac88184798e8c313e6ced23dd128f13ab30c199b96bd9c0bee07dbdd31400",
            "https://developer.download.nvidia.com/compute/cuda/12.6.1/local_installers/cuda_12.6.1_560.35.03_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "73acce7243519625f259509f5dcff6dc8fbd23dca53b852aa9ce382009e92e9d",
            "https://developer.download.nvidia.com/compute/cuda/12.6.1/local_installers/cuda_12.6.1_560.35.03_linux.run",
        ),
    },
    "12.6.0": {
        "Linux-aarch64": (
            "398db7baca17d51ad5035c606714c96380c965fd1742478c743bc6bbb1d8f63c",
            "https://developer.download.nvidia.com/compute/cuda/12.6.0/local_installers/cuda_12.6.0_560.28.03_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "31ab04394e69b14dd8656e2b44c2877db1a0e898dff8a7546a4c628438101b94",
            "https://developer.download.nvidia.com/compute/cuda/12.6.0/local_installers/cuda_12.6.0_560.28.03_linux.run",
        ),
    },
    "12.5.1": {
        "Linux-aarch64": (
            "353e8abc52ca80adf05002b775c7b3a2d2feefcf1c25ae13f8757f9a11efba3e",
            "https://developer.download.nvidia.com/compute/cuda/12.5.1/local_installers/cuda_12.5.1_555.42.06_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "b5e0a779e089c86610051141c4cf498beef431858ec63398107391727ecbdb04",
            "https://developer.download.nvidia.com/compute/cuda/12.5.1/local_installers/cuda_12.5.1_555.42.06_linux.run",
        ),
    },
    "12.5.0": {
        "Linux-aarch64": (
            "e7b864c9ae27cef77cafc78614ec33cbb0a27606af9375deffa09c4269a07f04",
            "https://developer.download.nvidia.com/compute/cuda/12.5.0/local_installers/cuda_12.5.0_555.42.02_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "90fcc7df48226434065ff12a4372136b40b9a4cbf0c8602bb763b745f22b7a99",
            "https://developer.download.nvidia.com/compute/cuda/12.5.0/local_installers/cuda_12.5.0_555.42.02_linux.run",
        ),
    },
    "12.4.1": {
        "Linux-aarch64": (
            "b0fbc77effa225498974625b6b08b3f6eff4a37e379f5b60f1d3827b215ad19b",
            "https://developer.download.nvidia.com/compute/cuda/12.4.1/local_installers/cuda_12.4.1_550.54.15_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "367d2299b3a4588ab487a6d27276ca5d9ead6e394904f18bccb9e12433b9c4fb",
            "https://developer.download.nvidia.com/compute/cuda/12.4.1/local_installers/cuda_12.4.1_550.54.15_linux.run",
        ),
        "Linux-ppc64le": (
            "677f44da10dd81396cb53a32c4e26eccdc24912063cb2e3beb3bbcb1658ef451",
            "https://developer.download.nvidia.com/compute/cuda/12.4.1/local_installers/cuda_12.4.1_550.54.15_linux_ppc64le.run",
        ),
    },
    "12.4.0": {
        "Linux-aarch64": (
            "b12bfe6c36d32ecf009a6efb0024325c5fc389fca1143f5f377ae2555936e803",
            "https://developer.download.nvidia.com/compute/cuda/12.4.0/local_installers/cuda_12.4.0_550.54.14_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "e6a842f4eca9490575cdb68b6b1bb78d47b95a897de48dee292c431892e57d17",
            "https://developer.download.nvidia.com/compute/cuda/12.4.0/local_installers/cuda_12.4.0_550.54.14_linux.run",
            "https://developer.download.nvidia.com/compute/cuda/11.6.2/local_installers/cuda_11.6.2_510.47.03_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "99b7a73dcc52a52cef4c1fceb4a60c3015ac9b6404082c1677d9efdaba1d4593",
            "https://developer.download.nvidia.com/compute/cuda/11.6.2/local_installers/cuda_11.6.2_510.47.03_linux.run",
        ),
        "Linux-ppc64le": (
            "869232ff8dbf295a71609738ac9e1b0079ca75597b427f1c026f42b36896afe8",
            "https://developer.download.nvidia.com/compute/cuda/11.6.2/local_installers/cuda_11.6.2_510.47.03_linux_ppc64le.run",
        ),
    },
    "11.6.1": {
        "Linux-aarch64": (
            "80586b003d58030004d465f5331dc69ee26c95a29516fb2488ff10f034139cb2",
            "https://developer.download.nvidia.com/compute/cuda/11.6.1/local_installers/cuda_11.6.1_510.47.03_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "ab219afce00b74200113269866fbff75ead037bcfc23551a8338c2684c984d7e",
            "https://developer.download.nvidia.com/compute/cuda/11.6.1/local_installers/cuda_11.6.1_510.47.03_linux.run",
        ),
        "Linux-ppc64le": (
            "ef762efbc00b67d572823c6ec338cc2c0cf0c096f41e6bce18e8d4501f260956",
            "https://developer.download.nvidia.com/compute/cuda/11.6.1/local_installers/cuda_11.6.1_510.47.03_linux_ppc64le.run",
        ),
    },
    "11.6.0": {
        "Linux-aarch64": (
            "5898579f5e59b708520883cb161089f5e4f3426158d1e9f973c49d224085d1d2",
            "https://developer.download.nvidia.com/compute/cuda/11.6.0/local_installers/cuda_11.6.0_510.39.01_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "1783da6d63970786040980b57fa3cb6420142159fc7d0e66f8f05c4905d98c83",
            "https://developer.download.nvidia.com/compute/cuda/11.6.0/local_installers/cuda_11.6.0_510.39.01_linux.run",
        ),
        "Linux-ppc64le": (
            "c86b866a42baf59ddc6f1f4a79e6d77213c90749e77e574f0e0d796a749ab7d0",
            "https://developer.download.nvidia.com/compute/cuda/11.6.0/local_installers/cuda_11.6.0_510.39.01_linux_ppc64le.run",
        ),
    },
    "11.5.2": {
        "Linux-aarch64": (
            "31337c8bdc224fa1bd07bc4b6a745798392428118cc8ea0fa4446ee4ad47dd30",
            "https://developer.download.nvidia.com/compute/cuda/11.5.2/local_installers/cuda_11.5.2_495.29.05_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "74959abf02bcba526f0a3aae322c7641b25da040ccd6236d07038f81997b73a6",
            "https://developer.download.nvidia.com/compute/cuda/11.5.2/local_installers/cuda_11.5.2_495.29.05_linux.run",
        ),
        "Linux-ppc64le": (
            "45c468f430436b3e95d5e485a6ba0ec1fa2b23dc6c551c1307b79996ecf0a7ed",
            "https://developer.download.nvidia.com/compute/cuda/11.5.2/local_installers/cuda_11.5.2_495.29.05_linux_ppc64le.run",
        ),
    },
    "11.5.1": {
        "Linux-aarch64": (
            "73e1d0e97c7fa686efe7e00fb1e5f179372c4eec8e14d4f44ab58d5f6cf57f63",
            "https://developer.download.nvidia.com/compute/cuda/11.5.1/local_installers/cuda_11.5.1_495.29.05_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "60bea2fc0fac95574015f865355afbf599422ec2c85554f5f052b292711a4bca",
            "https://developer.download.nvidia.com/compute/cuda/11.5.1/local_installers/cuda_11.5.1_495.29.05_linux.run",
        ),
        "Linux-ppc64le": (
            "9e0e494d945634fe8ad3e12d7b91806aa4220ed27487bb211030d651b27c67a9",
            "https://developer.download.nvidia.com/compute/cuda/11.5.1/local_installers/cuda_11.5.1_495.29.05_linux_ppc64le.run",
        ),
    },
    "11.5.0": {
        "Linux-aarch64": (
            "6ea9d520cc956cc751a5ac54f4acc39109627f4e614dd0b1a82cc86f2aa7d8c4",
            "https://developer.download.nvidia.com/compute/cuda/11.5.0/local_installers/cuda_11.5.0_495.29.05_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "ae0a1693d9497cf3d81e6948943e3794636900db71c98d58eefdacaf7f1a1e4c",
            "https://developer.download.nvidia.com/compute/cuda/11.5.0/local_installers/cuda_11.5.0_495.29.05_linux.run",
        ),
        "Linux-ppc64le": (
            "95baefdc5adf165189407b119861ffb2e9800fd94d7fc81d10fb81ed36dc12db",
            "https://developer.download.nvidia.com/compute/cuda/11.5.0/local_installers/cuda_11.5.0_495.29.05_linux_ppc64le.run",
        ),
    },
    "11.4.4": {
        "Linux-aarch64": (
            "c5c08531e48e8fdc2704fa1c1f7195f2c7edd2ee10a466d0e24d05b77d109435",
            "https://developer.download.nvidia.com/compute/cuda/11.4.4/local_installers/cuda_11.4.4_470.82.01_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "44545a7abb4b66dfc201dcad787b5e8352e5b7ddf3e3cc5b2e9177af419c25c8",
            "https://developer.download.nvidia.com/compute/cuda/11.4.4/local_installers/cuda_11.4.4_470.82.01_linux.run",
        ),
        "Linux-ppc64le": (
            "c71cd4e6c05fde11c0485369a73e7f356080e7a18f0e3ad7244e8fc03a9dd3e2",
            "https://developer.download.nvidia.com/compute/cuda/11.4.4/local_installers/cuda_11.4.4_470.82.01_linux_ppc64le.run",
        ),
    },
    "11.4.3": {
        "Linux-aarch64": (
            "e02db34a487ea3de3eec9db80efd09f12eb69d55aca686cecaeae96a9747b1d4",
        ),
    },
    "11.0.3": {
        "Linux-aarch64": (
            "1e24f61f79c1043aa3d1d126ff6158daa03a62a51b5195a2ed5fbe75c3b718f3",
            "https://developer.download.nvidia.com/compute/cuda/11.0.3/local_installers/cuda_11.0.3_450.51.06_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "b079c4e408adf88c3f1ffb8418a97dc4227c37935676b4bf4ca0beec6c328cc0",
            "https://developer.download.nvidia.com/compute/cuda/11.0.3/local_installers/cuda_11.0.3_450.51.06_linux.run",
        ),
        "Linux-ppc64le": (
            "4775b21df004b1433bafff9b48a324075c008509f4c0fe28cd060d042d2e0794",
            "https://developer.download.nvidia.com/compute/cuda/11.0.3/local_installers/cuda_11.0.3_450.51.06_linux_ppc64le.run",
        ),
    },
    "11.0.2": {
        "Linux-aarch64": (
            "23851e30f7c47a1baad92891abde0adbc783de5962c7480b9725198ceacda4a0",
            "https://developer.download.nvidia.com/compute/cuda/11.0.2/local_installers/cuda_11.0.2_450.51.05_linux_sbsa.run",
        ),
        "Linux-x86_64": (
            "48247ada0e3f106051029ae8f70fbd0c238040f58b0880e55026374a959a69c1",
            "https://developer.download.nvidia.com/compute/cuda/11.0.2/local_installers/cuda_11.0.2_450.51.05_linux.run",
        ),
        "Linux-ppc64le": (
            "db06d0f3fbf6f7aa1f106fc921ad1c86162210a26e8cb65b171c5240a3bf75da",
            "https://developer.download.nvidia.com/compute/cuda/11.0.2/local_installers/cuda_11.0.2_450.51.05_linux_ppc64le.run",
        ),
    },
    "10.2.89": {
        "Linux-x86_64": (
            "560d07fdcf4a46717f2242948cd4f92c5f9b6fc7eae10dd996614da913d5ca11",
            "https://developer.download.nvidia.com/compute/cuda/10.2/Prod/local_installers/cuda_10.2.89_440.33.01_linux.run",
        ),
        "Linux-ppc64le": (
            "5227774fcb8b10bd2d8714f0a716a75d7a2df240a9f2a49beb76710b1c0fc619",
            "https://developer.download.nvidia.com/compute/cuda/10.2/Prod/local_installers/cuda_10.2.89_440.33.01_linux_ppc64le.run",
        ),
    },
    "10.1.243": {
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
