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
        version("5.5.1", sha256="a6e67a95a7a5711a2b5f95f38ccbff4912262b3e1b1af7d6b9afe8185aa85c0d")
        version("5.5.0", sha256="1b619e326ff574de808732ca9a7447e4cd14e94ae6568f55b6581896cd569dff")

    variant("python", default=False, description="Enable Python support", when="@5.8:")
    variant("fortran", default=False, description="Enable Fortran support")
    variant("mpi", default=True, description="Enable MPI support")
    variant("qt", default=False, description="Enable Qt (gui) support")
    variant("opengl2", default=True, description="Enable OpenGL2 backend", when="@5:5")
    variant("x", default=True, description="Enable X11 support")
    variant("examples", default=False, description="Build examples")
    variant("hdf5", default=False, description="Use external HDF5")
    variant("shared", default=True, description="Builds a shared version of the library")
    variant("kits", default=True, description="Use module kits")
    variant("pagosa", default=False, description="Build the pagosa adaptor")
    variant("eyedomelighting", default=False, description="Enable Eye Dome Lighting feature")
    variant("tbb", default=False, description="Enable multi-threaded parallelism with TBB")
    variant("adios2", default=False, description="Enable ADIOS2 support", when="@5.8:")
    variant("fides", default=False, description="Enable Fides support", when="@5.9:")
    variant("visitbridge", default=False, description="Enable VisItBridge support")
    variant("raytracing", default=False, description="Enable Raytracing support")
    variant("cdi", default=False, description="Enable CDI support")
    variant(
        "openpmd",
        default=False,
        description="Enable openPMD support (w/ ADIOS2/HDF5)",
        when="@5.9: +python",
    )
    variant("catalyst", default=False, description="Enable Catalyst 1", when="@5.7:")
    variant(
        "libcatalyst",
        default=False,
        description="Enable Catalyst 2 (libcatalyst) implementation",
        when="@5.10:",
    )

    variant(
        "advanced_debug",
        default=False,
        description="Enable all other debug flags beside build_type, such as VTK_DEBUG_LEAK",
    )
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
    # before 5.3.0, ParaView didn't have VTK-m/Viskores



    # This affects Paraview <= 5.7 (VTK 8.2.0)
    # https://gitlab.kitware.com/vtk/vtk/-/issues/17670

    depends_on("py-numpy", when="+python", type=("build", "run"))
    depends_on("py-mpi4py", when="+python+mpi", type=("build", "run"))

    depends_on("py-matplotlib", when="+python", type="run")
    # openPMD is implemented as a Python module and provides ADIOS2 and HDF5 backends
    depends_on("openpmd-api@0.14.5: +python", when="+python +openpmd", type=("build", "run"))
    depends_on("openpmd-api +adios2", when="+openpmd +adios2", type=("build", "run"))
    depends_on("openpmd-api +hdf5", when="+openpmd +hdf5", type=("build", "run"))



    # Handle X11 dependencies
    # X is only used on Unix like platforms
    # When on linux, X is required for Qt
    for plat in ["linux", "freebsd"]:
        with when(f"platform={plat}"):
            requires("+x", when="+qt", msg="Qt support requires GLX on Linux/FreeBSD")

    with when("+x"):
        # When Qt and X are enabled, GLX is required in the runtime
        depends_on("glx", when="@6:", type=("run"))

    # ParaView@:5 support Qt5 and requires a GL provider to be known at
    # build/link time.
    with when("@:5"):
        with when("+qt"):
            depends_on("qt@:4", when="@:5.2.0")
            # https://discourse.paraview.org/t/paraview-5-9-and-minimum-recommended-qt-version/5333
            # Headless rendering not supported with Qt
            conflicts("osmesa")
            conflicts("egl")

        depends_on("gl@3.2:", when="+opengl2")
        depends_on("gl@1.2:", when="~opengl2")

        for _arch in ("10", "11", "12", "13"):
            conflicts(f"cuda_arch={_arch}", when="+cuda", msg="ParaView requires cuda_arch >= 20")

        # Starting from cmake@3.18, CUDA architecture managament can be delegated to CMake.
        # Hence, it is possible to rely on it instead of relying on custom logic updates from
        # VTK-m for newer architectures (wrt mapping).
        pattern = re.compile(r"\d+")
        for _arch in CudaPackage.cuda_arch_values:
            _number = re.match(pattern, _arch).group()
            if int(_number) > 86:
                conflicts("cmake@:3.17", when=f"cuda_arch={_arch}")

        # We only support one single Architecture
        for _arch, _other_arch in itertools.permutations(CudaPackage.cuda_arch_values, 2):
            conflicts(
                "cuda_arch={0}".format(_arch),
                when="cuda_arch={0}".format(_other_arch),
                msg="Paraview only accepts one architecture value",
            )

        # Dependencies for vendored VTK-m
        depends_on("hip@5.2:", when="+rocm")
        # CUDA thrust is already include in the CUDA pkg
        depends_on("rocthrust", when="@5.13: +rocm ^cmake@3.24:")
        for target in ROCmPackage.amdgpu_targets:
            depends_on(
                "kokkos@:3.7 +rocm amdgpu_target={0}".format(target),
                when="+rocm amdgpu_target={0}".format(target),
            )

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
        # * the system rendering default (WGL/AGL/GLX)
        # * EGL
        # * OSMesa (guarenteed to exist and work on all systems)
        for vk_variant in viskores_dependency_variants:
            depends_on("viskores +vtktypes +64bitids +doubleprecision", when=f"{vk_variant}")
            depends_on("viskores +fpic", when=f"+shared {vk_variant}")
        with when("+cuda"):
            # Kokkos vs Viskores Native CUDA is intentionally left configurable
            for _arch in CudaPackage.cuda_arch_values:
                depends_on(f"viskores cuda_arch={_arch}", when=f"cuda_arch={_arch}")
        with when("+rocm"):
            depends_on("viskores +rocm")
            for target in ROCmPackage.amdgpu_targets:
                depends_on(f"viskores amdgpu_target={target}", when=f"amdgpu_target={target}")

    depends_on("ospray@2.1:2", when="+raytracing")

    # depends_on('hdf5+mpi', when='+mpi')
    # depends_on('hdf5~mpi', when='~mpi')

    # and pre-5.9 is unable to handle that.
    # ParaView depends on cli11 due to changes in MR
    # https://gitlab.kitware.com/paraview/paraview/-/merge_requests/4951

    # ParaView depends on nlohmann-json due to changes in MR
    # https://gitlab.kitware.com/vtk/vtk/-/merge_requests/8550

    # ParaView depends on proj@8.1.0 due to changes in MR
    # v8.1.0 is required for VTK::GeoVis
    # https://gitlab.kitware.com/vtk/vtk/-/merge_requests/8474
    depends_on("proj@8.1.0", when="@5.11:")

    # Patches to vendored VTK-m are needed for forward compat with CUDA 12 (mr 2972 and 3259)
    depends_on("cuda@:11", when="@5.3:5.12 +cuda")
    patch("stl-reader-pv440.patch", when="@4.4.0")

    # Broken vtk-m config. Upstream catalyst changes
    # Broken downstream FindMPI
    patch("vtkm-findmpi-downstream.patch", when="@5.9.0")
    # Include limits header wherever needed to fix compilation with GCC 11
    patch("paraview-gcc11-limits.patch", when="@5.8:5.9 %gcc@11.1.0:")
    # Patch for paraview 5.9.0%xl_r

    # intel oneapi doesn't compile some code in catalyst
    # Fix VTK to remove deprecated ADIOS2 functions

    # https://github.com/Kitware/VTK-m/commit/c805a6039ea500cb96158cfc11271987c9f67aa4

    def test_pvpython(self):
        """Test pvpython"""
        if "~python" in self.spec:
            raise SkipTest("Package must be installed with +python")

        pvpython = Executable(self.prefix.bin.pvpython)
        pvpython("-c", "import paraview")

    def test_mpi_ensemble(self):
        """Test MPI ParaView Client/Server ensemble"""
        spec = self.spec

