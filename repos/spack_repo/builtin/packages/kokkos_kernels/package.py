# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.build_systems.cuda import CudaPackage

from spack.package import *


class KokkosKernels(CMakePackage, CudaPackage):
    """Kokkos Kernels provides math kernels, often BLAS or LAPACK
    for small matrices, that can be used in larger Kokkos parallel routines"""

    homepage = "https://github.com/kokkos/kokkos-kernels"
    git = "https://github.com/kokkos/kokkos-kernels.git"
    url = "https://github.com/kokkos/kokkos-kernels/releases/download/4.4.01/kokkos-kernels-4.4.01.tar.gz"

    tags = ["e4s"]

    test_requires_compiler = True





    variant("shared", default=True, description="Build shared libraries")
    variant(
        "execspace_cuda",
        default=False,
        description="Whether to pre instantiate kernels for the execution space Kokkos::Cuda",
    )
    variant(
        "execspace_openmp",
        default=False,
        description="Whether to pre instantiate kernels for the execution space "
        "Kokkos::Experimental::OpenMPTarget",
    )
    variant(
        "execspace_threads",
        default=False,
        description="Whether to pre instantiate kernels for the execution space Kokkos::Threads",
    )
    variant(
        "execspace_serial",
        default=False,
        description="Whether to pre instantiate kernels for the execution space Kokkos::Serial",
    )
    variant(
        "memspace_cudauvmspace",
        default=False,
        description="Whether to pre instantiate kernels for the memory space Kokkos::CudaUVMSpace",
    )
    variant(
        "memspace_cudaspace",
        default=False,
        description="Whether to pre instantiate kernels for the memory space Kokkos::CudaSpace",
    )
    variant("serial", default=False, description="Enable serial backend")
    variant("openmp", default=False, description="Enable OpenMP backend")
    variant("threads", default=False, description="Enable C++ threads backend")
    variant(
        "ordinals", default="int", values=["int", "int64_t"], multi=True, description="Ordinals"
    )
    variant(
        "offsets",
        default="int,size_t",
        values=["int", "size_t"],
        multi=True,
        description="Offsets",
    )
    variant("layouts", default="left", values=["left", "right"], description="Layouts")
    variant(
        "scalars",
        default="double",
        values=["float", "double", "complex_float", "complex_double"],
        multi=True,
        description="Scalars",
    )

    depends_on("cxx", type="build")
    for tpl in ("blas", "mkl"):
        depends_on("c", type="build", when=f"+{tpl}")
        depends_on("fortran", type="build", when=f"+{tpl}")
    depends_on("kokkos")
    depends_on("kokkos@develop", when="@develop")
    depends_on("kokkos@5.0.2", when="@5.0.2")
    depends_on("kokkos@5.0.1", when="@5.0.1")
    depends_on("kokkos@5.0.0", when="@5.0.0")
    depends_on("kokkos@4.7.02", when="@4.7.02")
    depends_on("kokkos@4.7.01", when="@4.7.01")
    depends_on("kokkos@4.7.00", when="@4.7.00")
    depends_on("kokkos@4.6.02", when="@4.6.02")
    depends_on("kokkos@4.6.01", when="@4.6.01")
    depends_on("kokkos@4.6.00", when="@4.6.00")
    depends_on("kokkos@4.5.01", when="@4.5.01")
    depends_on("kokkos@4.5.00", when="@4.5.00")
    depends_on("kokkos@4.4.01", when="@4.4.01")
    depends_on("kokkos@4.4.00", when="@4.4.00")
    depends_on("kokkos@4.3.01", when="@4.3.01")
    depends_on("kokkos@4.3.00", when="@4.3.00")
    depends_on("kokkos@4.2.01", when="@4.2.01")
    depends_on("kokkos@4.2.00", when="@4.2.00")
    depends_on("kokkos@4.1.00", when="@4.1.00")
    depends_on("kokkos@4.0.01", when="@4.0.01")
    depends_on("kokkos@4.0.00", when="@4.0.00")
    depends_on("kokkos@3.7.02", when="@3.7.02")
    depends_on("kokkos+pic", when="+shared")
    depends_on("kokkos+cuda", when="+execspace_cuda")
    depends_on("kokkos+openmp", when="+execspace_openmp")
    depends_on("kokkos+threads", when="+execspace_threads")
    depends_on("kokkos+serial", when="+execspace_serial")
    depends_on("kokkos+cuda", when="+memspace_cudauvmspace")
    depends_on("kokkos+cuda", when="+memspace_cudaspace")
    depends_on("kokkos+serial", when="+serial")
    depends_on("kokkos+cuda", when="+cuda")
    depends_on("kokkos+openmp", when="+openmp")
    depends_on("kokkos+threads", when="+threads")
    depends_on("kokkos+cuda_lambda", when="@4+cuda")
    depends_on("cmake@3.16:", type="build")

    tpls = {
        # variant name   #deflt   #spack name  #root var name  #supporting versions  #docstring
        "blas": (False, "blas", "BLAS", "@3.0.00:", "Link to system BLAS"),
        "lapack": (False, "lapack", "LAPACK", "@3.0.00:", "Link to system LAPACK"),
        "mkl": (False, "mkl", "MKL", "@3.0.00:", "Link to system MKL"),
        "cublas": (False, "cuda", None, "@3.0.00:", "Link to CUDA BLAS library"),
        "cusparse": (False, "cuda", None, "@3.0.00:", "Link to CUDA sparse library"),
        "superlu": (False, "superlu", "SUPERLU", "@3.1.00:", "Link to SuperLU library"),
        "cblas": (False, "cblas", "CBLAS", "@3.1.00:", "Link to CBLAS library"),
        "lapacke": (False, "clapack", "LAPACKE", "@3.1.00:", "Link to LAPACKE library"),
        "rocblas": (False, "rocblas", "ROCBLAS", "@3.6.00:", "Link to AMD BLAS library"),
        "rocsparse": (False, "rocsparse", "ROCSPARSE", "@3.6.00:", "Link to AMD sparse library"),
        "cusolver": (False, "cuda", None, "@4.3.00:", "Link to CUDA solver library"),
        "rocsolver": (False, "rocsolver", "ROCSOLVER", "@4.3.00:", "Link to AMD solver library"),
    }

    for tpl in tpls:
        deflt_bool, spackname, rootname, condition, descr = tpls[tpl]
        variant(tpl, default=deflt_bool, when=f"{condition}", description=descr)
        depends_on(spackname, when=f"+{tpl}")

    # lapack TPL depends on blas TPL
    conflicts("+lapack", when="~blas")

    patch("pr_2296_430.patch", when="@4.3.00:4.4.00")
    patch("pr_2296_400.patch", when="@4.0.00:4.2.01")

    # sanity check
    sanity_check_is_file = [join_path("include", "KokkosKernels_config.h")]
    sanity_check_is_dir = ["include"]

    def cmake_args(self):
        spec = self.spec
        options = [
            self.define_from_variant("KokkosKernels_INST_EXECSPACE_CUDA", "execspace_cuda"),
            self.define_from_variant("KokkosKernels_INST_EXECSPACE_OPENMP", "execspace_openmp"),
            self.define_from_variant("KokkosKernels_INST_EXECSPACE_THREADS", "execspace_threads"),
            self.define_from_variant("KokkosKernels_INST_EXECSPACE_SERIAL", "execspace_serial"),
            self.define_from_variant("KokkosKernels_INST_EXECSPACE_SERIAL", "execspace_serial"),
            self.define_from_variant(
                "KokkosKernels_INST_MEMSPACE_CUDAUVMSPACE", "memspace_cudauvmspace"
            ),
            self.define_from_variant(
                "KokkosKernels_INST_MEMSPACE_CUDASPACE", "memspace_cudaspace"
            ),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
        ]

        options.append(self.define("Kokkos_ROOT", spec["kokkos"].prefix))
        if spec.satisfies("^kokkos+rocm"):
            options.append(self.define("CMAKE_CXX_COMPILER", spec["hip"].hipcc))
        else:
            options.append(self.define("CMAKE_CXX_COMPILER", self["kokkos"].kokkos_cxx))

        if self.run_tests:
            options.append(self.define("KokkosKernels_ENABLE_TESTS", True))

        for tpl in self.tpls:
            dflt, spackname, rootname, condition, descr = self.tpls[tpl]
            if spec.satisfies(f"+{tpl}"):
                options.append(self.define(f"KokkosKernels_ENABLE_TPL_{tpl.upper()}", True))
                if rootname:
                    options.append(self.define(f"{rootname}_ROOT", spec[spackname].prefix))
                else:
                    pass

        for val in spec.variants["ordinals"].value:
            options.append(self.define(f"KokkosKernels_INST_ORDINAL_{val.upper()}", True))
        for val in spec.variants["offsets"].value:
            options.append(self.define(f"KokkosKernels_INST_OFFSET_{val.upper()}", True))
        for val in spec.variants["scalars"].value:
            options.append(self.define(f"KokkosKernels_INST_{val.upper()}", True))
        layout_value = spec.variants["layouts"].value
        options.append(self.define(f"KokkosKernels_INST_LAYOUT{layout_value.upper()}", True))

        return options
