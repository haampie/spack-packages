# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.packages.boost.package import Boost

from spack.package import *


class Metall(CMakePackage):
    """A Persistent Memory Allocator For Data-Centric Analytics"""

    homepage = "https://github.com/LLNL/metall"
    git = "https://github.com/LLNL/metall.git"
    url = "https://github.com/LLNL/metall/archive/refs/tags/v0.20.tar.gz"

    maintainers("KIwabuchi", "rogerpearce", "mayagokhale")

    tags = ["e4s"]

    license("MIT")

    version("master", branch="master")
    version("develop", branch="develop")

    version("0.30", sha256="d241f45978fceeb83a4b2eda7513466341c45452fa26ec224c5235d00d279d37")
    version("0.29", sha256="03281b603b46703c324971798819242529431cbbdaa80d5dbb5f0f8a24a74a58")
    version("0.28", sha256="770dedb7f8220c333688b232a22104ca9d8d5823e7a8a21152b58ef970eb85d0")
    version("0.27", sha256="6e6f17a760778f9162def939701f9381a75e5275fd1eb1b2af4b2e89e86e1c58")
    version("0.26", sha256="7453c87d99708be8542e354e582cbeefac1e5ba65e609cd85d7126c5b25a6d7b")
    version("0.25", sha256="223cb54543b62a62fdbbe6274b02ddcc14b29806e344ee7e2fd3f055c2374295")
    version("0.24", sha256="872de2a1b76d44e6876c0b672c0cc518c6f334959e4a229f2f18cc7e01edf477")
    version("0.23.1", sha256="25e8fbc424e66d09e0faf60029288e4612685675bfd947cc142bd9d6d0645ac4")
    version("0.23", sha256="17987922a3eb23a6b904498858db94aca12859d5dbcd8483704619ae93353340")
    version("0.18", sha256="cd1fee376d0523d43e43b92c43731d45a2c4324278a071a5f626f400afecef24")
    version("0.17", sha256="8de6ec2a430a141a2ad465ccd40ba9d0eb0c57d9f2f2de657fe837a73c466e61")
    version("0.16", sha256="190fa6936cbbfad1844659eb1fcfd1ad8c5880f60e76e223e33c506d371ea3a3")
    version("0.15", sha256="a1ea475ce1297b0c4cdf450544dc60ecf1b0a30c548b08ba77ccda5585df7248")
    version("0.14", sha256="386a6db0cfd3b3693cf8b0de323dcb60d43777aa5c871b744c9e8c19a572a917")
    version("0.10", sha256="58b4b5507d4db5baca315b1bed2b728981755d755b91ef63bd0b6dfaf320f46b")
    version("0.9", sha256="2d7bd9ea2f1e04136050f210884445a9e3dcb96c992cf42ff9ea4b392f85f927")



    # googletest is required only for test
    # GCC is also required only for test (Metall is a header-only library)
    # Hint: Use 'spack install --test=root metall' or 'spack install --test=all metall'
    # to run test (adds a call to 'make test' to the build)
    depends_on("googletest %gcc@8.1.0:", type=("test"))

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, type=("build", "link"))

    def cmake_args(self):
        if self.run_tests:
            args = ["-DBUILD_TEST=ON", "-DSKIP_DOWNLOAD_GTEST=ON"]
            return args
        else:
            args = ["-DINSTALL_HEADER_ONLY=ON"]
            return args

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        # Configure the directories for test
        if self.run_tests:
            env.set("METALL_TEST_DIR", join_path(self.build_directory, "build_test"))

    # 'spack load metall' sets METALL_ROOT environmental variable
    def setup_run_environment(self, env: EnvironmentModifications) -> None:
        env.set("METALL_ROOT", self.prefix)
