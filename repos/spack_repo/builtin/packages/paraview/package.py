import sys
from subprocess import Popen
from spack_repo.builtin.build_systems.cmake import CMakePackage, generator
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.rocm import ROCmPackage
from spack.package import *
IS_WINDOWS = sys.platform == "win32"
class Paraview(CMakePackage, CudaPackage, ROCmPackage):
    git = "https://gitlab.kitware.com/paraview/paraview.git"
    tags = ["e4s"]
    with default_args(deprecated=True):
        version("5.4.0", sha256="f488d84a53b1286d2ee1967e386626c8ad05a6fe4e6cbdaa8d5e042f519f94a9")
        version("4.4.0", sha256="c2dc334a89df24ce5233b81b74740fc9f10bc181cd604109fd13f6ad2381fc73")
    variant("qt", default=False, description="Enable Qt (gui) support")
    variant("opengl2", default=True, description="Enable OpenGL2 backend", when="@5:5")
    with when("@6:"):
            depends_on("qt-tools+assistant")
