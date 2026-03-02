import os
import re
import sys
from subprocess import Popen
from spack_repo.builtin.build_systems.cmake import CMakePackage, generator
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.rocm import ROCmPackage
from spack.package import *
IS_WINDOWS = sys.platform == "win32"
# This is (more or less) the mapping hard-coded in VTK-m logic
# see https://gitlab.kitware.com/vtk/vtk-m/-/blob/v2.1.0/CMake/VTKmDeviceAdapters.cmake?ref_type=tags#L221-247
supported_cuda_archs = {
    "86": "ampere",
}
# This is a list of paraview variants that require the viskores library.
viskores_dependency_variants = ["+cuda", "+fides", "+rocm"]
class Paraview(CMakePackage, CudaPackage, ROCmPackage):
    """ParaView is an open-source, multi-platform data analysis and
    """
    homepage = "https://www.paraview.org"
    variant("mpi", default=True, description="Enable MPI support")
    variant("qt", default=False, description="Enable Qt (gui) support")
    variant("visitbridge", default=False, description="Enable VisItBridge support")
    variant("raytracing", default=False, description="Enable Raytracing support")
    variant("cdi", default=False, description="Enable CDI support")
    variant(
        "build_edition",
        default="canonical",
        multi=False,
        values=("canonical", "catalyst_rendering", "catalyst", "rendering", "core"),
        description="Build editions include only certain modules. "
        "Editions are listed in decreasing order of size.",
    )
    variant(
        "use_vtkm",
        default="default",
        description="Build VTK-m with ParaView."
        ' "default" lets the build_edition make the decision.'
        ' "on" or "off" will always override the build_edition.',
    )
    # Legacy rendering dropped in 5.5
    # See commit: https://gitlab.kitware.com/paraview/paraview/-/commit/798d328c
    # in 5.7 you cannot reduce the size of the code for Catalyst builds.
    conflicts("build_edition=catalyst", when="@:5.7")
    with when("@6:"):
            depends_on("qt-tools+assistant")
            depends_on("qt-5compat")
