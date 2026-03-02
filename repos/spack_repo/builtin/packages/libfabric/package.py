# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.rocm import ROCmPackage

from spack.package import *


class Libfabric(AutotoolsPackage, CudaPackage, ROCmPackage):
    """The Open Fabrics Interfaces (OFI) is a framework focused on exporting
    fabric communication services to applications."""

    homepage = "https://libfabric.org/"
    url = "https://github.com/ofiwg/libfabric/releases/download/v1.8.0/libfabric-1.8.0.tar.bz2"
    git = "https://github.com/ofiwg/libfabric.git"

    executables = ["^fi_info$"]


    version("1.5.3", sha256="f62a40da06f8951db267a59a4ee7363b6ee60a7abbc55cd5db6c8b067d93fa0c")
    version("1.5.0", sha256="88a8ad6772f11d83e5b6f7152a908ffcb237af273a74a1bd1cb4202f577f1f23")
    version("1.4.2", sha256="5d027d7e4e34cb62508803e51d6bd2f477932ad68948996429df2bfff37ca2a5")

    fabrics = (
        "cxi",
        "efa",
        "gni",
        "lnx",
        "mlx",
        "mrail",
        "opx",
        "psm",
        "psm2",
        "psm3",
        "rxm",
        "rxd",
        "shm",
        "sockets",
        "tcp",
        "ucx",
        "udp",
        "usnic",
        "verbs",
        "xpmem",
    )

    variant(
        "fabrics",
        default="sockets,tcp,udp",
        description="A list of enabled fabrics",
        values=fabrics,
        multi=True,
    )

    # NOTE: the 'kdreg' variant enables use of the special /dev/kdreg2 file to
    #   assist in memory registration caching in the GNI provider.  This
    #   device file can only be opened once per process, however, and thus it
    #   frequently conflicts with MPI.
    variant("kdreg", default=False, description="Enable kdreg2 on supported Cray platforms")
    variant("debug", default=False, description="Enable debugging")
    variant("uring", default=False, when="@1.17.0:", description="Enable uring support")
    variant("level_zero", default=False, description="Enable Level Zero support")
    variant("gdrcopy", default=False, when="@1.12: +cuda", description="Enable gdrcopy support")
    variant(
        "cuda_dlopen", default=False, when="+cuda", description="Enable dlopen of CUDA libraries"
    )

    variant(
        "ubsan",
        default=False,
        when="@1.20:",
        description="Enable UndefinedBehaviorSanitizer (UBSan)",
    )

    # Backporting from main for versions 2.3.x
    # The CXI provider hardcodes CXIP_FI_VERSION to FI_VERSION(2, 2).
    # Make it match the libfabric we're building

    # For version 1.9.0:
    # headers: fix forward-declaration of enum fi_collective_op with C++
    depends_on("rdma-core", when="fabrics=verbs")
    depends_on("rdma-core", when="@1.10.0: fabrics=efa")
    depends_on("opa-psm2", when="fabrics=psm2")
    depends_on("cxi-driver", when="fabrics=cxi")
    depends_on("xpmem", when="fabrics=xpmem")

    conflicts("fabrics=opx", when="@:1.14.99")

    flag_handler = build_system_flags

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"libfabric: (\d+\.\d+\.\d+)(\D*\S*)", output)
        return match.group(1) if match else None

        results = []
        for exe in exes:
            output = Executable(exe)("--list", output=str, error=os.devnull)
            # fabrics
            used_fabrics = []
            for fabric in cls.fabrics:
                match = re.search(r"^%s:.*\n.*version: (\S+)" % fabric, output, re.MULTILINE)
                if match:
                    used_fabrics.append(fabric)
            if used_fabrics:
                variants.append("fabrics=" + ",".join(used_fabrics))
            results.append(" ".join(variants))
        return results

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        if self.run_tests:
            env.prepend_path("PATH", self.prefix.bin)

    # To enable this package add it to the LD_LIBRARY_PATH
    def setup_run_environment(self, env: EnvironmentModifications) -> None:
        env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib)
        env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib64)

    # To enable this package add it to the LD_LIBRARY_PATH
    def setup_dependent_run_environment(
        self, env: EnvironmentModifications, dependent_spec: Spec
    ) -> None:
        env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib)
        env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib64)

    @when("@main")
    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./autogen.sh")

    def configure_args(self):
        args = [
            *self.enable_or_disable("debug"),
            *self.enable_or_disable("cuda_dlopen"),
            *self.enable_or_disable("gdrcopy_dlopen"),
            *self.enable_or_disable("asan"),
            *self.enable_or_disable("lsan"),
            *self.enable_or_disable("tsan"),
            *self.enable_or_disable("ubsan"),
            *self.with_or_without("uring"),
            *self.with_or_without("cuda", activation_value="prefix"),
            *self.with_or_without("ze", variant="level_zero"),
            *self.with_or_without("gdrcopy", activation_value="prefix"),
            *self.with_or_without(
                "rocr", variant="rocm", activation_value=lambda _: self.spec["hip"].prefix
            ),
        ]

        if self.spec.satisfies("+kdreg"):
            args.append("--with-kdreg2")

        for fabric in [f if isinstance(f, str) else f[0].value for f in self.fabrics]:
            if f"fabrics={fabric}" in self.spec:
                if fabric == "xpmem":
                    args.append(f"--enable-xpmem={self.spec['xpmem'].prefix}")
                elif fabric == "cxi":
                    args.append(f"--with-json-c={self.spec['json-c'].prefix}")
                    args.append(f"--with-curl={self.spec['curl'].prefix}")
                    args.append(
                        f"--with-cassini-headers={self.spec['cassini-headers'].prefix.include}"
                    )
                    args.append(
                        f"--with-cxi-uapi-headers={self.spec['cxi-driver'].prefix.include}"
                    )
                    args.append(f"--enable-cxi={self.spec['libcxi'].prefix}")
                else:
                    args.append(f"--enable-{fabric}")
            else:
                args.append(f"--disable-{fabric}")

        return args

    def installcheck(self):
        fi_info = Executable(self.prefix.bin.fi_info)
        fi_info()
