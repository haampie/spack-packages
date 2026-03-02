# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import os.path
import pathlib
import platform
import warnings
from spack_repo.builtin.build_systems.compiler import CompilerPackage
from spack_repo.builtin.build_systems.oneapi import IntelOneApiPackage
from spack.package import *
versions = [
    {
        "version": "2025.3.2",
        "cpp": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/0d61d48a-4fe8-4cb2-bd9d-94d2c19c6227/intel-dpcpp-cpp-compiler-2025.3.2.26_offline.sh",
            "sha256": "37d6c9c22f90fbb4d2072fd45d0284f2b6b1ffd030d699e1e7a669087d093396",
        },
        "ftn": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/3e53d136-2870-4836-adb1-892b558fa34a/intel-fortran-compiler-2025.3.2.25_offline.sh",
            "sha256": "c64d20d70a277b1249d2ba9221be7245a843f3988df9076b4456619fe5929278",
        },
    },
    {
        "version": "2025.3.1",
        "cpp": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/5adfc398-db78-488c-b98f-78461b3c5760/intel-dpcpp-cpp-compiler-2025.3.1.16_offline.sh",
            "sha256": "b0e8920fa390302133b0e92784389ae383806d8414c48ae8b9e2f2ed1ad72471",
        },
        "ftn": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/724303ca-6927-4327-a560-e0aabb55b010/intel-fortran-compiler-2025.3.1.16_offline.sh",
            "sha256": "13138cca7df96469d7f707428de6e2cf23a98a49ac01ea0b80c7623c0f474d43",
        },
    },
    {
        "version": "2025.3.0",
        "cpp": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/44809add-596f-4484-9cd1-cc032460e241/intel-dpcpp-cpp-compiler-2025.3.0.322_offline.sh",
            "sha256": "a85dc98ac76d16522d387cf62dc3b712b863779cb74520d8e37ea282ea02ef63",
        },
        "ftn": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/b3aa3ab5-c79d-4af4-8801-983ef00b90fd/intel-fortran-compiler-2025.3.0.325_offline.sh",
            "sha256": "ede518607ce625051321989c843af9cebdbdc9ab07c8dbb2f011463e4e18678b",
        },
    },
    {
        "version": "2025.2.2",
        "cpp": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/95aea65e-ead3-402f-838c-53d9f7bbaf3c/intel-dpcpp-cpp-compiler-2025.2.2.10_offline.sh",
            "sha256": "f143aa4df3ce4add7efb795ae53482120407009607bc8924fb25b9325b5ed39f",
        },
        "ftn": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/05fdb0f1-5c91-4bdc-af11-cf7afe0c02fe/intel-fortran-compiler-2025.2.2.10_offline.sh",
            "sha256": "8ddd51baab30e3370ab41ce2ad38d4c3a1455d2354715ccc7392d4b655ba6bc9",
        },
    },
    {
        "version": "2025.2.1",
        "cpp": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/04c5fd98-57e6-4a4b-be4d-e84de3aea45a/intel-dpcpp-cpp-compiler-2025.2.1.7_offline.sh",
            "sha256": "028ef9e2176289bab6b9d19828199d26cb6cd91babdcfcece7a9dd00c5a50376",
        },
        "ftn": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/466b0d65-e502-4172-9e06-24c565029b96/intel-fortran-compiler-2025.2.1.9_offline.sh",
            "sha256": "75165cc737d164cda2c068e0d8ec4f269f005a50bc2e254cd3cab6fdd063e145",
        },
    },
    {
        "version": "2025.2.0",
        "cpp": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/39c79383-66bf-4f44-a6dd-14366e34e255/intel-dpcpp-cpp-compiler-2025.2.0.527_offline.sh",
            "sha256": "aea3c1ccb97728db138b4f11f771411264292ba7bbec313782229510c9b831bc",
        },
        "ftn": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/2c69ab6a-dfff-4d8f-ae1c-8368c79a1709/intel-fortran-compiler-2025.2.0.534_offline.sh",
            "sha256": "3808000bbcef15f17b608156b956e0114393a1b64ee6d9fb29be06450fa40083",
        },
    },
    {
        "version": "2025.1.1",
        "cpp": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/c4d2aef3-3123-475e-800c-7d66fd8da2a5/intel-dpcpp-cpp-compiler-2025.1.1.9_offline.sh",
            "sha256": "63ea61f54a5ea9d30059ea499697e04953915ef317c0e8fc457077b690c726df",
        },
        "ftn": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/0e4735b3-8721-422b-b204-00eefe413bfd/intel-fortran-compiler-2025.1.1.10_offline.sh",
            "sha256": "c59060a5b959fb0faeb1cde349689086da41d491adb41fd6c97177fcf59bf957",
        },
    },
    {
        "version": "2025.1.0",
        "cpp": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/cd63be99-88b0-4981-bea1-2034fe17f5cf/intel-dpcpp-cpp-compiler-2025.1.0.573_offline.sh",
            "sha256": "53489afcc9534e30ad807e94b158abfccf6a7eb3658f59655122d92fbad8fa72",
        },
        "ftn": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/577ebc28-d0f6-492b-9a43-b04354ce99da/intel-fortran-compiler-2025.1.0.601_offline.sh",
            "sha256": "27016329dede8369679f22b4e9f67936837ce7972a1ef4f5c76ee87d7c963c81",
        },
    },
    {
        "version": "2025.0.4",
        "cpp": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/84c039b6-2b7d-4544-a745-3fcf8afd643f/intel-dpcpp-cpp-compiler-2025.0.4.20_offline.sh",
            "sha256": "0537c6e462fe74063cb0b9209a0fd5c0ca3a29b4520d43d382ae27fb3f98b375",
        },
        "ftn": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/ad42ee3b-7a2f-41cb-b902-689f651920da/intel-fortran-compiler-2025.0.4.21_offline.sh",
            "sha256": "ad453f1dd68111e7cf7053d6f86fa26d982bd9ab61982cbb6dbe5195fb6feedb",
        },
    },
    {
        "version": "2025.0.3",
        "cpp": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/1cac4f39-2032-4aa9-86d7-e4f3e40e4277/intel-dpcpp-cpp-compiler-2025.0.3.9_offline.sh",
            "sha256": "0ca834002b9091dc9988da6798a2eb36ebc5933d8d523ed0fa78a55744c88823",
        },
        "ftn": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/fafa2df1-4bb1-43f7-87c6-3c82f1bdc712/intel-fortran-compiler-2025.0.3.9_offline.sh",
            "sha256": "1ad813cf6495ded730646d6c4fd065dcc840875fdea28fcc6bac2cafb8d22c8d",
        },
    },
    {
        "version": "2025.0.1",
        "cpp": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/4fd7c6b0-853f-458a-a8ec-421ab50a80a6/intel-dpcpp-cpp-compiler-2025.0.1.46_offline.sh",
            "sha256": "1595397566b59a5c8f81e2c235b6bedd2405dc70309b5bf00ed75827d0f12449",
        },
        "ftn": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/6780ac84-6256-4b59-a647-330eb65f32b6/l_dpcpp-cpp-compiler_p_2024.2.0.495_offline.sh",
            "sha256": "9463aa979314d2acc51472d414ffcee032e9869ca85ac6ff4c71d39500e5173d",
        },
        "ftn": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/801143de-6c01-4181-9911-57e00fe40181/l_fortran-compiler_p_2024.2.0.426_offline.sh",
            "sha256": "fd19a302662b2f86f76fc115ef53a69f16488080278dba4c573cc705f3a52ffa",
        },
        "nvidia-plugin": {
            "url": "https://developer.codeplay.com/api/v1/products/download?product=oneapi&variant=nvidia&version=2024.2.0&filters[]=12.0&filters[]=linux",
            "sha256": "0622df0054364b01e91e7ed72a33cb3281e281db5b0e86579f516b1cc5336b0f",
        },
        "amd-plugin": {
            "url": "https://developer.codeplay.com/api/v1/products/download?product=oneapi&variant=amd&version=2024.2.0&filters[]=6.1.0&filters[]=linux",
            "sha256": "d1e9d30fa92f3ef606f054d8cbd7c338b3e46f6a9f8472736e29e8ccd9e50688",
        },
    },
    {
        "version": "2024.1.0",
        "cpp": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/2e562b6e-5d0f-4001-8121-350a828332fb/l_dpcpp-cpp-compiler_p_2024.1.0.468_offline.sh",
            "sha256": "534ecc6e4b690c9011d7765cbe178f520aa8f49c0eb4ea80ea1415e48e5d7cf7",
        },
        "ftn": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/fd9342bd-7d50-442c-a3e4-f41974e14396/l_fortran-compiler_p_2024.1.0.465_offline.sh",
            "sha256": "30a02bad9a96a543c60f3bfa4238dfe07c2d26d76fc22ba9aa9b7c603e11f1b9",
        },
    },
    {
        "version": "2024.0.2",
        "cpp": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/bb99984f-370f-413d-bbec-38928d2458f2/l_dpcpp-cpp-compiler_p_2024.0.2.29_offline.sh",
            "sha256": "0ec22d69f4207fea4b7488d1c9e62adbc14fb6daa1574d6edcadc912da007b3c",
        },
        "ftn": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/41df6814-ec4b-4698-a14d-421ee2b02aa7/l_fortran-compiler_p_2024.0.2.28_offline.sh",
            "sha256": "396ac4fbcb3799d5c1a866a60cf81f85f7cab8c6f35289f61c5cda63c7101b5e",
        },
    },
    {
        "version": "2024.0.1",
        "cpp": {
            "sha256": "c4553f7e707be8e8e196f625e4e7fbc8eff5474f64ab85fc7146b5ed53ebc87c",
        },
    },
    {
        "version": "2021.2.0",
        "cpp": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/17749/l_dpcpp-cpp-compiler_p_2021.2.0.118_offline.sh",
            "sha256": "5d01cbff1a574c3775510cd97ffddd27fdf56d06a6b0c89a826fb23da4336d59",
        },
        "ftn": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/17756/l_fortran-compiler_p_2021.2.0.136_offline.sh",
            "sha256": "a62e04a80f6d2f05e67cd5acb03fa58857ee22c6bd581ec0651c0ccd5bdec5a1",
        },
    },
    {
        "version": "2021.1.2",
        "cpp": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/17513/l_dpcpp-cpp-compiler_p_2021.1.2.63_offline.sh",
            "sha256": "68d6cb638091990e578e358131c859f3bbbbfbf975c581fd0b4b4d36476d6f0a",
        },
        "ftn": {
            "url": "https://registrationcenter-download.intel.com/akdlm/IRC_NAS/17508/l_fortran-compiler_p_2021.1.2.62_offline.sh",
            "sha256": "29345145268d08a59fa7eb6e58c7522768466dd98f6d9754540d1a0803596829",
        },
    },
]
@IntelOneApiPackage.update_description
class IntelOneapiCompilers(IntelOneApiPackage, CompilerPackage):
    """Intel oneAPI Compilers. Includes: icx, icpx, ifx, and ifort.
    Releases before 2024.0 include icc/icpc"""
    homepage = "https://software.intel.com/content/www/us/en/develop/tools/oneapi.html"
    compiler_languages = ["c", "cxx", "fortran"]
    c_names = ["icx"]
    cxx_names = ["icpx"]
    fortran_names = ["ifx"]
    compiler_version_argument = "--version"
    compiler_version_regex = (
        r"(?:(?:oneAPI DPC\+\+(?:\/C\+\+)? Compiler)|(?:\(IFORT\))|(?:\(IFX\))) (\S+)"
    )
    debug_flags = ["-debug", "-g", "-g0", "-g1", "-g2", "-g3"]
    opt_flags = ["-O", "-O0", "-O1", "-O2", "-O3", "-Ofast", "-Os"]
    openmp_flag = "-fiopenmp"
    compiler_wrapper_link_paths = {
        "c": os.path.join("oneapi", "icx"),
        "cxx": os.path.join("oneapi", "icpx"),
        "fortran": os.path.join("oneapi", "ifx"),
    }
    implicit_rpath_libs = [
        "libirc",
        "libifcore",
        "libifcoremt",
        "libirng",
        "libsvml",
        "libintlc",
        "libimf",
        "libsycl",
        "libOpenCL",
    ]
    stdcxx_libs = ("-cxxlib",)
    provides("c", "cxx")
    # See https://github.com/spack/spack/issues/39252
    depends_on("patchelf@:0.17", type="build", when="@:2024.1")
    # Add the nvidia variant
    # Add the amd variant
    for v in versions:
        version(v["version"], expand=False, **v["cpp"])
        if "ftn" in v:
            resource(
                name="fortran-installer",
                placement="fortran-installer",
                when="@{0}".format(v["version"]),
                expand=False,
                **v["ftn"],
            )
        if "nvidia-plugin" in v:
            resource(
                name="nvidia-plugin-installer",
                placement="nvidia-plugin-installer",
                when="@{0}+nvidia".format(v["version"]),
                expand=False,
                **v["nvidia-plugin"],
            )
        if "amd-plugin" in v:
            resource(
                name="amd-plugin-installer",
                placement="amd-plugin-installer",
                when="@{0}+amd".format(v["version"]),
                expand=False,
                **v["amd-plugin"],
            )
