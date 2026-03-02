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
