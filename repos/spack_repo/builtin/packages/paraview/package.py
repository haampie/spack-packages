from spack_repo.builtin.build_systems.cmake import CMakePackage, generator
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.rocm import ROCmPackage
from spack.package import *
class Paraview(CMakePackage, CudaPackage, ROCmPackage):
    variant(
        "build_edition",
        default="canonical",
        values=("canonical", "catalyst_rendering", "catalyst", "rendering", "core"),
        description="Build editions include only certain modules. "
        "Editions are listed in decreasing order of size.",
    )
    with when("@6:"):
            depends_on("qt-tools+assistant")
            depends_on("qt-5compat")
