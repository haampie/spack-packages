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


    version("1.18.1", sha256="4615ae1e22009e59c72ae03c20adbdbd4a3dce95aeefbc86cc2bf1acc81c9e38")
    version("1.18.0", sha256="912fb7c7b3cf2a91140520962b004a1c5d2f39184adbbd98ae5919b0178afd43")
    version("1.17.1", sha256="8b372ddb3f46784c53fdad50a701a6eb0e661239aee45a42169afbedf3644035")
    version("1.17.0", sha256="579c0f5ef636c0c72f4d3d6bd4da91a5aed9ac3ac4ea387404c45dbbdee4745d")
    version("1.16.1", sha256="53f992d33f9afe94b8a4ea3d105504887f4311cf4b68cea99a24a85fcc39193f")
    version("1.16.0", sha256="ac104b9d6e3ce8bda6116329e3f440b621d85602257b3015116ca590f65267d2")
    version("1.15.2", sha256="8d050b88bee62e8512a88f5aa25f532f46bef587bc3f91022ecdb9b3b2676c7e")
    version("1.15.1", sha256="cafa3005a9dc86064de179b0af4798ad30b46b2f862fe0268db03d13943e10cd")
    version("1.15.0", sha256="70982c58eadeeb5b1ddb28413fd645e40b206618b56fbb2b18ab1e7f607c9bea")
    version("1.14.1", sha256="6cfabb94bca8e419d9015212506f5a367d077c5b11e94b9f57997ec6ca3d8aed")
    version("1.14.0", sha256="fc261388848f3cff555bd653f5cb901f6b9485ad285e5c53328b13f0e69f749a")
    version("1.13.2", sha256="25d783b0722a8df8fe61c1de75fafca684c5fe520303180f26f0ad6409cfc0b9")
    version("1.13.1", sha256="8e6eed38c4a39aa4cbf7d5d3734f0eecbfc030182f1f9b3be470702f2586d30e")
    version("1.12.1", sha256="db3c8e0a495e6e9da6a7436adab905468aedfbd4579ee3da5232a5c111ba642c")

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
        "gdrcopy_dlopen",
        default=False,
        when="+gdrcopy",
        description="Enable dlopen of gdr libraries",
    )

    variant("asan", default=False, when="@1.12:", description="Enable AddressSanitizer (ASan)")
    variant("lsan", default=False, when="@1.20:", description="Enable LeakSanitizer (LSan)")
    variant("tsan", default=False, when="@1.20:", description="Enable ThreadSanitizer (TSan)")
    variant(
        "ubsan",
        default=False,
        when="@1.20:",
        description="Enable UndefinedBehaviorSanitizer (UBSan)",
    )

    # Backporting from main for versions 2.3.x
    # The CXI provider hardcodes CXIP_FI_VERSION to FI_VERSION(2, 2).
    # Make it match the libfabric we're building
    patch(
        "https://github.com/ofiwg/libfabric/commit/f565852cedc7b6fd3848ed2f11b1dd90ed37be05.patch?full_index=1",
        sha256="da2514252074c350fb5cbdb04f267cf227d0a575902fe6cad355afe1dc7c0102",
        when="@2.3 fabrics=cxi",
    )

    # For version 1.9.0:
    # headers: fix forward-declaration of enum fi_collective_op with C++
    patch(
        "https://github.com/ofiwg/libfabric/commit/2e95b0efd85fa8a3d814128e34ec57ffd357460e.patch?full_index=1",
        sha256="456693e28bb1fc41a0bbb94b97ae054e7d28f81ca94795d7f294243da58c6376",
        when="@1.9.0",
    )

    # Fix for the inline assembly problem for the Nvidia compilers
    # https://github.com/ofiwg/libfabric/pull/7665
    patch("nvhpc-symver.patch", when="@1.6.0:1.14.0 %nvhpc")



    depends_on("autoconf", when="@main", type="build")
    depends_on("automake", when="@main", type="build")
    depends_on("libtool", when="@main", type="build")
    depends_on("json-c", when="fabrics=cxi")
    depends_on("curl", when="fabrics=cxi")



    flag_handler = build_system_flags

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"libfabric: (\d+\.\d+\.\d+)(\D*\S*)", output)
        return match.group(1) if match else None

    @classmethod
    def determine_variants(cls, exes, version):
        results = []
        for exe in exes:
            variants = []
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
