import os
import sys
from spack_repo.builtin.build_systems.cmake import CMakeBuilder, CMakePackage
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.rocm import ROCmPackage
from spack.package import *
IS_WINDOWS = sys.platform == "win32"
class Adios2(CMakePackage, CudaPackage, ROCmPackage):
    """The Adaptable Input Output System version 2,
    developed in the Exascale Computing Program"""
