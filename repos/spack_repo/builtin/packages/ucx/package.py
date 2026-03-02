# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import shutil

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.cuda import CudaPackage

from spack.package import *


class Ucx(AutotoolsPackage, CudaPackage):
    """a communication library implementing high-performance messaging for
    MPI/PGAS frameworks"""

    homepage = "https://www.openucx.org"
    url = "https://github.com/openucx/ucx/releases/download/v1.3.1/ucx-1.3.1.tar.gz"
    git = "https://github.com/openucx/ucx.git"




    # Current

    # Still supported

    # Retired

    simd_values = ("avx", "sse41", "sse42")

    variant("assertions", default=False, description="Enable assertions")
    variant(
        "backtrace_detail",
        default=False,
        description="Enable using BFD support "
        "for detailed backtrace. Note: this adds a dependency on binutils, you may "
        "want to mark binutils as external or depend on binutils~ld to avoid "
        "changing the linker during the build of ucx.",
    )
    variant("debug", default=False, description="Enable debugging")
    variant("examples", default=True, description="Keep examples")
    variant("java", default=False, description="Builds with Java bindings")
    variant(
        "libs",
        default="shared,static",
        values=("shared", "static"),
        multi=True,
        description="Build shared libs, static libs or both",
    )
    variant("logging", default=False, description="Enable logging")
    variant("numa", default=True, when="@:1.14", description="Enable NUMA support")
    variant("openmp", default=True, description="Use OpenMP")
    variant("rocm", default=False, description="Enable ROCm support")
    variant(
        "simd",
        description="SIMD features",
        values=disjoint_sets(("auto",), simd_values)
        .with_default("auto")
        .with_non_feature_values("auto"),
    )
    variant("thread_multiple", default=False, description="Enable thread support in UCP and UCT")
    variant(
        "ucg",
        default=False,
        description="Enable the group collective operations (experimental component)",
    )

    variant("dm", default=False, description="Compile with Device Memory support")
    variant("gdrcopy", default=False, description="Enable gdrcopy support")
    variant("ib_hw_tm", default=False, description="Compile with IB Tag Matching support")
    variant("knem", default=False, description="Enable KNEM support")
    variant("mlx5_dv", default=False, description="Compile with mlx5 Direct Verbs support")
    variant("rc", default=False, description="Compile with IB Reliable Connection support")
    variant("rdmacm", default=False, description="Enable the use of RDMACM")
    variant("ud", default=False, description="Compile with IB Unreliable Datagram support")
    variant("verbs", default=False, description="Build OpenFabrics support")
    variant("xpmem", default=False, description="Enable XPMEM support")
    variant("gtest", default=False, description="Build and install Googletest")


    depends_on("gdrcopy", when="@1.7:+gdrcopy")
    depends_on("gdrcopy@1.3", when="@:1.6+gdrcopy")
    depends_on("java@8", when="+java")
    depends_on("knem", when="+knem")
    depends_on("rdma-core", when="+rdmacm")
    depends_on("rdma-core", when="+verbs")
    depends_on("xpmem", when="+xpmem")
    depends_on("hip", when="+rocm")
    depends_on("hsa-rocr-dev", when="+rocm")

    conflicts("+gdrcopy", when="~cuda", msg="gdrcopy currently requires cuda support")
    conflicts("+rocm", when="+gdrcopy", msg="gdrcopy > 2.0 does not support rocm")

    # https://github.com/openucx/ucx/issues/10589
    conflicts("%gcc@15:", when="@:1.18")

    configure_abs_path = "contrib/configure-release"

    # See https://github.com/openucx/ucx/pull/8629, wrong int type

    def configure_args(self):
        spec = self.spec
        args = ["--without-go", "--disable-doxygen-doc"]  # todo  # todo

        args += self.enable_or_disable("numa")
        args += self.enable_or_disable("assertions")
        args.append("--enable-compiler-opt=" + self.spec.variants["opt"].value)
        args += self.with_or_without("java", activation_value="prefix")
        args += self.enable_or_disable("libs")
        args += self.enable_or_disable("logging")
        args += self.enable_or_disable("mt", variant="thread_multiple")
        args += self.with_or_without("openmp")
        args += self.enable_or_disable("optimizations")
        args += self.enable_or_disable("params-check", variant="parameter_checking")
        args += self.enable_or_disable("gtest")
        args += self.with_or_without("pic")

        args += self.with_or_without("cuda", activation_value="prefix")

        args += self.with_or_without("cm")
        args += self.enable_or_disable("cma")
        args += self.with_or_without("dc")
        args += self.with_or_without("dm")
        args += self.with_or_without("gdrcopy", activation_value="prefix")
        args += self.with_or_without("ib-hw-tm", variant="ib_hw_tm")
        args += self.with_or_without("knem", activation_value="prefix")
        args += self.with_or_without("rc")
        args += self.with_or_without("ud")
        args += self.with_or_without("xpmem", activation_value="prefix")

        # mlx5_dv
        # UCX <= 1.17: --with-mlx5-dv
        # UCX >= 1.18: --with-mlx5
        if spec.satisfies("@:1.17"):
            args += self.with_or_without("mlx5-dv", variant="mlx5_dv")
        else:
            args += self.with_or_without("mlx5", variant="mlx5_dv")

        # Virtual filesystem as of UCX 1.11
        if "+vfs" in spec:
            args.append("--with-fuse3=" + self.spec["libfuse"].prefix)
        else:
            args.append("--without-fuse3")

        # Backtraces
        # UCX <= 1.11: --enable-backtrace-detail
        # UCX >= 1.12: --with-bfd
        if "@:1.11" in spec:
            args += self.enable_or_disable("backtrace-detail", variant="backtrace_detail")
        else:
            if "+backtrace_detail" in spec:
                args.append("--with-bfd=" + self.spec["binutils"].prefix)
            else:
                args.append("--without-bfd")

        if "+rdmacm" in spec:
            args.append("--with-rdmacm=" + self.spec["rdma-core"].prefix)
        else:
            args.append("--without-rdmacm")

        if "+verbs" in spec:
            args.append("--with-verbs=" + self.spec["rdma-core"].prefix)
        else:
            args.append("--without-verbs")

        # SIMD flags.
        if self.spec.satisfies("simd=auto"):
            if "avx" in self.spec.target:
                args.append("--with-avx")
            else:
                args.append("--without-avx")
        elif self.spec.satisfies("simd=none"):
            for instr in self.simd_values:
                args.append("--without-" + instr)
        else:
            for instr in self.simd_values:
                if instr in spec.variants["simd"].value:
                    args.append("--with-" + instr)
                else:
                    args.append("--without-" + instr)

        # lld doesn't support '-dynamic-list-data'
        if "%aocc" in spec:
            args.append("LDFLAGS=-fuse-ld=bfd")

        if "+rocm" in spec:
            cppflags = " ".join(
                "-I" + include_dir
                for include_dir in (
                    self.spec["hip"].prefix.include,
                    self.spec["hip"].prefix.include.hip,
                    self.spec["hsa-rocr-dev"].prefix.include.hsa,
                )
            )
            ldflags = " ".join(
                "-L" + library_dir
                for library_dir in (
                    self.spec["hip"].prefix.lib,
                    self.spec["hsa-rocr-dev"].prefix.lib,
                )
            )
            args.extend(["CPPFLAGS=" + cppflags, "LDFLAGS=" + ldflags])
            args.append("--with-rocm=" + self.spec["hip"].prefix)
        else:
            args.append("--without-rocm")

        return args

    @run_after("install")
    def drop_examples(self):
        if self.spec.satisfies("~examples"):
            shutil.rmtree(join_path(self.spec.prefix, "share", "ucx", "examples"))

    @run_after("install")
    def install_gtest(self):
        if self.spec.satisfies("+gtest"):
            install_tree("test", self.spec.prefix.test)
