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

    version("2.9.1", sha256="a440e2299f7451dc10a57ddbfa3f116c2a6c4be1bb97c663edd3b9c7b3b3b4cf")
    version("2.9.0", sha256="9d7d3450e0a5fea4cb80ca07dc8db939abb7ab62e2a7bb27f9376447658738ec")
    version("2.8.0", sha256="20b2bd4df436827d8e50f7afeafb6f967259f2fb374ce7330244f8d0ed2dde6f")
    version("2.7.1", sha256="4cb0a781ed980b03ad8c48beb57407aa67c4b908e45722954b9730379bc7f6d5")
    version("2.7.0", sha256="d9b23e9b0d17247e8b50254810427ca8a9857dc868e2e3a049f958d7c66af374")
    version("2.6.0", sha256="9aa7e768ed4fd429f488466a311ef2191054ea96ea1a68657bc06ffbb745e59f")
    version("2.5.0", sha256="38aa8102faec302791f6b4f0d23960a3ffa25af3af6af006c64dbecac23f852c")
    version("2.4.1", sha256="4267fe1193a8989f3ab7563a7499e047e77e33fed8f4dec16822a7aebcf78459")
    version("2.4.0", sha256="30404065dc1d6872b0181269d0bb2424fbbc6e3b0a80491aa373109554006544")
    version("2.3.0", sha256="155480620c98b43ddf9ca66a6c318b363ca24acb5ff0683af9d25d9324f59836")
    version("2.2.0", sha256="2defba03ddd91761b858cbbdc2e3a6e27b44e94696dbfa21380191328485a433")

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
    depends_on("pkgconfig", type="build")
    depends_on("m4", type="build", when="@master")
    depends_on("autoconf", type="build", when="@master")
    depends_on("automake", type="build", when="@master")
    depends_on("libtool", type="build", when="@master")
    depends_on("cuda", when="+nvml")
    depends_on("cuda", when="+cuda")
    depends_on("gl", when="+gl")
    depends_on("libpciaccess", when="+pci")
    depends_on("libxml2", when="+libxml2")
    depends_on("cairo", when="+cairo")
    depends_on("numactl", when="@:1.11.11 platform=linux")
    depends_on("ncurses")

    # Before 2.2 hwloc does not consider linking to libtinfo
    # to detect ncurses, which is considered a bug.
    # For older versions this can be fixed by depending on
    # ncurses~termlib, but this could lead to insatisfiable
    # constraints (e.g. llvm explicitly depends on ncurses+termlib)
    # Therefore we patch the latest 1.x configure script to make
    # it consider libtinfo too.
    # see https://github.com/open-mpi/hwloc/pull/417
    patch("0001-Try-linking-to-libtinfo.patch", when="@1.11.13")
    depends_on("ncurses ~termlib", when="@2.0:2.2")
    depends_on("ncurses ~termlib", when="@1.0:1.11.12")

    # When mpi=openmpi, this introduces an unresolvable dependency.
    # See https://github.com/spack/spack/issues/15836 for details
    depends_on("mpi", when="+netloc")

    with when("+rocm"):
        depends_on("rocm-smi-lib")
        depends_on("rocm-opencl", when="+opencl")
        # Avoid a circular dependency since the openmp
        # variant of llvm-amdgpu depends on hwloc.
        depends_on("llvm-amdgpu", when="+opencl")

    with when("+level_zero"):
        depends_on("oneapi-level-zero")
        # LevelZero support isn't available until hwloc version 2.5.0
        conflicts("@:2.4", msg="hwloc supports Intel OneAPI Level Zero only since 2.5.0")

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"hwloc-bind (\S+)", output)
        return match.group(1) if match else None

    def url_for_version(self, version):
        url = "https://download.open-mpi.org/release/hwloc/v{0}/hwloc-{1}.tar.gz"
        return url.format(version.up_to(2), version)

    @property
    def libs(self):
        libs = find_libraries("libhwloc", root=self.prefix, shared=True, recursive=True)
        return LibraryList(libs)

    def configure_args(self):
        args = [
            *self.enable_or_disable("netloc"),
            *self.enable_or_disable("cairo"),
            *self.enable_or_disable("nvml"),
            *self.enable_or_disable("levelzero", variant="level_zero"),
        ]

        # If OpenCL is not enabled, disable it since hwloc might
        # pick up an OpenCL library at build time that is then
        # not found at run time.
        # The OpenCl variant allows OpenCl providers such as
        # 'cuda' and 'rocm-opencl' to be used.
        if "+opencl" not in self.spec:
            args.append("--disable-opencl")

        # If ROCm libraries are found in system /opt/rocm
        # during config stage, hwloc builds itself with
        # librocm_smi support.
        # This can fail the config tests while building
        # OpenMPI due to lack of rpath to librocm_smi
        if "+rocm" not in self.spec:
            args.append("--disable-rsmi")

        if self.spec.satisfies("+rocm"):
            args.append(f"--with-rocm={self.spec['hip'].prefix}")
            args.append(f"--with-rocm-version={self.spec['hip'].version}")

        if self.spec.satisfies("+cuda"):
            args.append(f"--with-cuda={self.spec['cuda'].prefix}")
            args.append(f"--with-cuda-version={self.spec['cuda'].version}")

        return args
