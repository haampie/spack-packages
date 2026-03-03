import sys
from subprocess import Popen
from spack_repo.builtin.build_systems.cmake import CMakePackage, generator
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.rocm import ROCmPackage
from spack.package import *
IS_WINDOWS = sys.platform == "win32"
class Paraview(CMakePackage, CudaPackage, ROCmPackage):
    git = "https://gitlab.kitware.com/paraview/paraview.git"
    with when("@6:"):
            depends_on("qt-tools+assistant")
