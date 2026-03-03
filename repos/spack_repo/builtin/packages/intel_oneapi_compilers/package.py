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
    provides("fortran")
    # See https://github.com/spack/spack/issues/39252
    # Add the nvidia variant
    variant("nvidia", default=False, description="Install NVIDIA plugin for OneAPI")
    conflicts("@:2022.2.1", when="+nvidia", msg="Codeplay NVIDIA plugin requires newer release")
    # Add the amd variant
    variant("amd", default=False, description="Install AMD plugin for OneAPI")
    conflicts("@:2022.2.1", when="+amd", msg="Codeplay AMD plugin requires newer release")
    for v in versions:
        version(v["version"], expand=False, **v["cpp"])
        if "ftn" in v:
            resource(
                name="fortran-installer",
                placement="fortran-installer",
                when="@{0}".format(v["version"]),
            )
