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



    executables = ["^hwloc-bind$"]

    version("2.9.3", sha256="5985db3a30bbe51234c2cd26ebe4ae9b4c3352ab788b1a464c40c0483bf4de59")
    version("2.9.2", sha256="ffb554d5735e0e0a19d1fd4b2b86e771d3b58b2d97f257eedacae67ade5054b3")
    version("2.9.1", sha256="a440e2299f7451dc10a57ddbfa3f116c2a6c4be1bb97c663edd3b9c7b3b3b4cf")
    version("2.9.0", sha256="9d7d3450e0a5fea4cb80ca07dc8db939abb7ab62e2a7bb27f9376447658738ec")
    version("2.4.1", sha256="4267fe1193a8989f3ab7563a7499e047e77e33fed8f4dec16822a7aebcf78459")
    version("2.4.0", sha256="30404065dc1d6872b0181269d0bb2424fbbc6e3b0a80491aa373109554006544")
    version("2.3.0", sha256="155480620c98b43ddf9ca66a6c318b363ca24acb5ff0683af9d25d9324f59836")
    version("2.2.0", sha256="2defba03ddd91761b858cbbdc2e3a6e27b44e94696dbfa21380191328485a433")
    version("2.1.0", sha256="1fb8cc1438de548e16ec3bb9e4b2abb9f7ce5656f71c0906583819fcfa8c2031")
    version("2.0.4", sha256="efadca880f5a59c6d5d6f7bc354546aa6f780d77cc2e139634c3de9564e7ce1f")
    version("2.0.3", sha256="64def246aaa5b3a6e411ce10932a22e2146c3031b735c8f94739534f06ad071c")
    version("2.0.2", sha256="27dcfe42e3fb3422b72ce48b48bf601c0a3e46e850ee72d9bdd17b5863b6e42c")
    version("1.11.7", sha256="ac16bed9cdd3c63bca1fe1ac3de522a1376b1487c4fc85b7b19592e28fd98e26")
    version("1.11.6", sha256="67963f15197e6b551539c4ed95a4f8882be9a16cf336300902004361cf89bdee")
    version("1.11.5", sha256="da2c780fce9b5440a1a7d1caf78f637feff9181a9d1ca090278cae4bea71b3df")
    version("1.9", sha256="9fb572daef35a1c8608d1a6232a4a9f56846bab2854c50562dfb9a7be294f4e8")

    variant("nvml", default=False, description="Support NVML device discovery")
    variant("gl", default=False, description="Support GL device discovery")
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
    depends_on("libtool", type="build", when="@master")
    depends_on("libxml2", when="+libxml2")
    depends_on("cairo", when="+cairo")
    depends_on("numactl", when="@:1.11.11 platform=linux")
    depends_on("ncurses")

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

