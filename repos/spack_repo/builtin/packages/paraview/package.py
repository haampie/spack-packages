# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import itertools
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
    "20": "fermi",
    "21": "fermi",
    "30": "kepler",
    "32": "kepler",
    "35": "kepler",
    "37": "kepler",
    "50": "maxwel",
    "52": "maxwel",
    "53": "maxwel",
    "60": "pascal",
    "61": "pascal",
    "62": "pascal",
    "70": "volta",
    "72": "volta",
    "75": "turing",
    "80": "ampere",
    "86": "ampere",
}
# This is a list of paraview variants that require the viskores library.
viskores_dependency_variants = ["+cuda", "+fides", "+rocm"]
class Paraview(CMakePackage, CudaPackage, ROCmPackage):
    """ParaView is an open-source, multi-platform data analysis and
    visualization application. This package includes the Catalyst
    in-situ library for versions 5.7 and greater, otherwise use the
    catalyst package.
    """
    homepage = "https://www.paraview.org"
    url = "https://www.paraview.org/files/v5.7/ParaView-v5.7.0.tar.xz"
    list_url = "https://www.paraview.org/files"
    list_depth = 1
    git = "https://gitlab.kitware.com/paraview/paraview.git"
    tags = ["e4s"]
    with default_args(deprecated=True):
        version("5.5.2", sha256="64561f34c4402b88f3cb20a956842394dde5838efd7ebb301157a837114a0e2d")
    variant("python", default=False, description="Enable Python support", when="@5.8:")
    variant("fortran", default=False, description="Enable Fortran support")
    variant("mpi", default=True, description="Enable MPI support")
    variant("qt", default=False, description="Enable Qt (gui) support")
    variant("opengl2", default=True, description="Enable OpenGL2 backend", when="@5:5")
    variant("x", default=True, description="Enable X11 support")
    variant("examples", default=False, description="Build examples")
    variant("hdf5", default=False, description="Use external HDF5")
    variant("shared", default=True, description="Builds a shared version of the library")
    variant("adios2", default=False, description="Enable ADIOS2 support", when="@5.8:")
    variant("fides", default=False, description="Enable Fides support", when="@5.9:")
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
        when="@5.3.0:5.13",
        multi=False,
        values=("default", "on", "off"),
        description="Build VTK-m with ParaView."
        ' "default" lets the build_edition make the decision.'
        ' "on" or "off" will always override the build_edition.',
    )
    # Legacy rendering dropped in 5.5
    # See commit: https://gitlab.kitware.com/paraview/paraview/-/commit/798d328c
    # in 5.7 you cannot reduce the size of the code for Catalyst builds.
    conflicts("build_edition=catalyst", when="@:5.7")
    with when("@6:"):
        # ParaView 6 and later will not support Spack builds with Qt5.
        with when("+qt"):
            depends_on("qt-base+accessibility+gui+opengl+sql+network")
            depends_on("qt-tools+assistant")
            depends_on("qt-5compat")
            depends_on("qt-svg")
            depends_on("libxslt")
        # OpenGL.
        # The search order for GL is:
