# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.build_systems.cuda import CudaPackage

from spack.package import *


class Spatter(CMakePackage, CudaPackage):
    """A microbenchmark for timing Gather/Scatter kernels on CPUs and GPUs."""

    homepage = "https://github.com/hpcgarage/spatter"
    git = "https://github.com/hpcgarage/spatter.git"

    maintainers("plavin", "jyoung3131")

    license("MIT", checked_by="plavin")

    version("develop", branch="spatter-devel")

    variant("cuda_arch", default="none", multi=True, description="CUDA architecture")

    depends_on("cmake@3.25:", type="build")
    depends_on("mpi", when="+mpi")
    depends_on("cuda", when="backend=cuda")

    conflicts(
        "backend=cuda",
        when="cuda_arch=none",
        msg="CUDA architecture must be specified when CUDA support is enabled.",
    )

    def cmake_args(self):
        args = []

        if self.spec.satisfies("backend=openmp"):
            args.append(self.define("USE_OPENMP", "On"))
        elif self.spec.satisfies("backend=cuda"):
            args.append(self.define("USE_CUDA", "On"))
            args.append(
                self.define("CMAKE_CUDA_ARCHITECTURES", self.spec.variants["cuda_arch"].value)
            )

        args.append(self.define_from_variant("USE_MPI", "mpi"))

        return args
