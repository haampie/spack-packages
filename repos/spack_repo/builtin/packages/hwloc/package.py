# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import sys

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.rocm import ROCmPackage

from spack.package import *


class Hwloc(AutotoolsPackage, CudaPackage, ROCmPackage):
    """The Hardware Locality (hwloc) software project.

    The Portable Hardware Locality (hwloc) software package
    provides a portable abstraction (across OS, versions,
    architectures, ...) of the hierarchical topology of modern
    architectures, including NUMA memory nodes, sockets, shared
    caches, cores and simultaneous multithreading. It also gathers
    various system attributes such as cache and memory information
    as well as the locality of I/O devices such as network
    interfaces, InfiniBand HCAs or GPUs. It primarily aims at
    helping applications with gathering information about modern
    computing hardware so as to exploit it accordingly and
    efficiently.
    """

    homepage = "https://www.open-mpi.org/projects/hwloc/"
    url = "https://download.open-mpi.org/release/hwloc/v2.11/hwloc-2.11.1.tar.bz2"
    git = "https://github.com/open-mpi/hwloc.git"



    variant("libxml2", default=True, description="Build with libxml2")
    variant("libudev", default=False, when="@1.11.0:", description="Build with libudev")
    variant(
        "pci",
        default=(sys.platform != "darwin"),
        description="Support analyzing devices on PCI bus",
    )
    variant(
        "libs",
        default="shared,static",
        values=("shared", "static"),
        multi=True,
        description="Build shared libs, static libs or both",
    )
    variant(
        "cairo", default=False, description="Enable the Cairo back-end of hwloc's lstopo command"
    )
    variant(
        "netloc", default=False, when="@2.0.0:2.9.3", description="Enable netloc [requires MPI]"
    )
    variant("opencl", default=False, description="Support an OpenCL library at run time")
    variant("rocm", default=False, description="Support ROCm devices")
    variant("level_zero", default=False, description="Support Intel OneAPI Level Zero devices")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("libxml2", when="+libxml2")

    # Before 2.2 hwloc does not consider linking to libtinfo
    # to detect ncurses, which is considered a bug.
    # For older versions this can be fixed by depending on
    # ncurses~termlib, but this could lead to insatisfiable
    # constraints (e.g. llvm explicitly depends on ncurses+termlib)

    # When mpi=openmpi, this introduces an unresolvable dependency.
    # See https://github.com/spack/spack/issues/15836 for details

    with when("+rocm"):
        depends_on("rocm-opencl", when="+opencl")
        # Avoid a circular dependency since the openmp
        # variant of llvm-amdgpu depends on hwloc.
        depends_on("llvm-amdgpu", when="+opencl")

    with when("+level_zero"):
        depends_on("oneapi-level-zero")
        # LevelZero support isn't available until hwloc version 2.5.0
        conflicts("@:2.4", msg="hwloc supports Intel OneAPI Level Zero only since 2.5.0")

