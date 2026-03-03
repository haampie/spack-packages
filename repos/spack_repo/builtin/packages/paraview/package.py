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
        version("5.4.1", sha256="390d0f5dc66bf432e202a39b1f34193af4bf8aad2355338fa5e2778ea07a80e4")
        version("5.4.0", sha256="f488d84a53b1286d2ee1967e386626c8ad05a6fe4e6cbdaa8d5e042f519f94a9")
        version("4.4.0", sha256="c2dc334a89df24ce5233b81b74740fc9f10bc181cd604109fd13f6ad2381fc73")

    variant(
        "development_files",
        default=True,
        description="Install include files for Catalyst or plugins support",
    )
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
    variant("adios2", default=False, description="Enable ADIOS2 support", when="@5.8:")
    variant("fides", default=False, description="Enable Fides support", when="@5.9:")
    variant("visitbridge", default=False, description="Enable VisItBridge support")
    variant("raytracing", default=False, description="Enable Raytracing support")
    variant("cdi", default=False, description="Enable CDI support")


    # Legacy rendering dropped in 5.5
    # See commit: https://gitlab.kitware.com/paraview/paraview/-/commit/798d328c
    # in 5.7 you cannot reduce the size of the code for Catalyst builds.
    # before 5.3.0, ParaView didn't have VTK-m/Viskores
    # paraview@5.9.0 is recommended when using the xl compiler
    # See https://gitlab.kitware.com/paraview/paraview/-/merge_requests/4433




    # VTK < 8.2.1 can't handle Python 3.8
    # This affects Paraview <= 5.7 (VTK 8.2.0)
    # https://gitlab.kitware.com/vtk/vtk/-/issues/17670



    # openPMD is implemented as a Python module and provides ADIOS2 and HDF5 backends



    # Handle X11 dependencies
    # X is only used on Unix like platforms
    # When on linux, X is required for Qt
    for plat in ["linux", "freebsd"]:
        with when(f"platform={plat}"):
            requires("+x", when="+qt", msg="Qt support requires GLX on Linux/FreeBSD")

    with when("+x"):
        # When Qt and X are enabled, GLX is required in the runtime
        requires("^[virtuals=gl] glx", when="@:5")

    # ParaView@:5 support Qt5 and requires a GL provider to be known at
    # build/link time.
    with when("@:5"):
        with when("+qt"):
            # https://discourse.paraview.org/t/paraview-5-9-and-minimum-recommended-qt-version/5333
            # Headless rendering not supported with Qt
            conflicts("osmesa")
            conflicts("egl")


        # CUDA ARCH

        # VTK-m and transitively ParaView does not support Tesla Arch
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

        # ParaView@6: and later will depend on OSMesa as a fallback for
        # OpenGL.
        # The search order for GL is:
        # * the system rendering default (WGL/AGL/GLX)
        # * EGL
        # * OSMesa (guarenteed to exist and work on all systems)
        depends_on("osmesa", type=("run"), when="~qt")

        # Depend on Viskores when it is needed
        for vk_variant in viskores_dependency_variants:
            depends_on("viskores +vtktypes +64bitids +doubleprecision", when=f"{vk_variant}")
            depends_on("viskores +fpic", when=f"+shared {vk_variant}")

        with when("+cuda"):
            # Kokkos vs Viskores Native CUDA is intentionally left configurable
            depends_on("viskores +cuda")
            for _arch in CudaPackage.cuda_arch_values:
                depends_on(f"viskores cuda_arch={_arch}", when=f"cuda_arch={_arch}")

        with when("+rocm"):
            depends_on("viskores +rocm")
            for target in ROCmPackage.amdgpu_targets:
                depends_on(f"viskores amdgpu_target={target}", when=f"amdgpu_target={target}")

    depends_on("ospray@2.1:2", when="+raytracing")
    depends_on("openimagedenoise", when="+raytracing")
    depends_on("ospray +mpi", when="+raytracing +mpi")

    depends_on("cdi", when="+cdi")

    # depends_on('hdf5~mpi', when='~mpi')
    # Paraview 5.10 can't build with protobuf > 3.18


    # Patches to vendored VTK-m are needed for forward compat with CUDA 12 (mr 2972 and 3259)

    # Broken downstream FindMPI

    # Fix IOADIOS2 module to work with kits

    # Patch for paraview 5.9.0%xl_r
    # https://gitlab.kitware.com/vtk/vtk/-/merge_requests/7591
    # intel oneapi doesn't compile some code in catalyst

    # Patch for paraview 5.8: ^hdf5@1.13.2:
    # https://gitlab.kitware.com/vtk/vtk/-/merge_requests/9690
    # a patch with the same name is also applied to vtk
    # the two patches are the same but for the path to the files they patch


    # Fix VTK to remove deprecated ADIOS2 functions



    # https://github.com/Kitware/VTK-m/commit/c805a6039ea500cb96158cfc11271987c9f67aa4

    # https://github.com/Kitware/VTK-m/commit/48e385af319543800398656645327243a29babfb

    # Vtk's findpegtl's include search is wrong: https://gitlab.kitware.com/vtk/vtk/-/issues/17876

    # https://gitlab.kitware.com/paraview/paraview/-/merge_requests/7593

    generator("ninja", "make", default="ninja")
    # https://gitlab.kitware.com/paraview/paraview/-/issues/21223
    conflicts("generator=ninja", when="%xl")
    conflicts("generator=ninja", when="%xl_r")

    # Versions 5.13.0-5.13.2 do not compile with Intel classic compilers
    conflicts("%intel", when="@5.13:5.13.2")

