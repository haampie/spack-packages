# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.build_systems.cuda import CudaPackage

from spack.package import *


class Autodiff(CMakePackage, CudaPackage):
    """autodiff is automatic differentiation made easier for C++."""

    homepage = "https://autodiff.github.io"
    url = "https://github.com/autodiff/autodiff/archive/refs/tags/v0.6.4.tar.gz"
    list_url = "https://github.com/autodiff/autodiff/tags"
    git = "https://github.com/autodiff/autodiff.git"

    maintainers("wdconinc")


    version("1.1.2", sha256="86f68aabdae1eed214bfbf0ddaa182c78ea1bb99e4df404efb7b94d30e06b744")
    version("1.1.1", sha256="05aa2a432c83db079efeca1c407166a3f3d190645bd3202da3b6357fb30fc9e1")
    version("1.1.0", sha256="a5489bb546c460af52de8ead447439b3c97429184df28b4d142ce7dcfd62b82c")
    version("1.0.3", sha256="21b57ce60864857913cacb856c3973ae10f7539b6bb00bcc04f85b2f00db0ce2")
    version("1.0.2", sha256="a3289aed937a39a817f76e6befa0d071a3e70a5b0b125ec62d1acf1d389e2197")
    version("1.0.1", sha256="63f2c8aaf940fbb1d1e7098b1d6c08794da0194eec3faf773f3123dc7233838c")
    version("1.0.0", sha256="112c6f5740071786b3f212c96896abc2089a74bca16b57bb46ebf4cec79dca43")
    version("0.6.12", sha256="3e9d667b81bba8e43bbe240a0321e25f4be248d1761097718664445306882dcc")
    version("0.6.7", sha256="1345021d74bfd34e74a58d98f4e0e16cc4666b6cd18628af0ba642a6521aadfa")
    version("0.6.6", sha256="2a4498b09da9a223b896a3bbfc9ebcb7c7c0b906b19a25000e6f3b94698d916d")
    version("0.6.5", sha256="252ced0f4e892e9957c67fe8bb1c9edd5636f121a8481abc0a0cec9a4c465484")
    version("0.6.4", sha256="cfe0bb7c0de10979caff9d9bfdad7e6267faea2b8d875027397486b47a7edd75")




    conflicts("+cuda", when="@:1.0", msg="CUDA support was added in 1.1.0")

    def cmake_args(self):
        args = [
            self.define("AUTODIFF_BUILD_TESTS", self.run_tests),
            self.define_from_variant("AUTODIFF_BUILD_PYTHON", "python"),
            self.define_from_variant("AUTODIFF_BUILD_EXAMPLES", "examples"),
        ]
        return args
