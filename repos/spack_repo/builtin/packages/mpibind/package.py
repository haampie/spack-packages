# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Mpibind(AutotoolsPackage):
    """A portable runtime library that automatically maps
    parallel applications to heterogeneous hardware architectures,
    optimizing resource affinity for CPUs, GPUs, and memory"""

    homepage = "https://mpibind.llnl.gov"
    git = "https://github.com/LLNL/mpibind.git"


    # This package uses 'git describe --tags' to get the
    # package version in Autotools' AC_INIT, thus
    # 'get_full_repo' is needed.
    # Furthermore, the package can't be cached because
    # AC_INIT would be missing the version argument,
    # which is derived with git.


    # mpibind does not depend on CUDA or ROCm, but uses
    # these variants to configure hwloc accordingly
    variant("cuda", default=False, description="Build with support for NVIDIA GPUs")
    variant("rocm", default=False, description="Build with support for AMD GPUs")

    variant("flux", default=False, description="Build the Flux plugin")
    variant("python", default=False, description="Build the Python bindings")

    # See slurm dependency below
    # variant("slurm", default=False,
    #         description="Build the Slurm plugin")





    # Need mpibind v0.23+ and hwloc v2.12+ for NV Grace Hopper
    conflicts(
        "@:0.22 +cuda target=neoverse_v2:", msg="version 0.23+ is needed for NVIDIA Grace Hopper"
    )

    # flux-core >= 0.30.0 supports FLUX_SHELL_RC_PATH,
    # which is needed to load the plugin into Flux

    # The slurm spack package does not provide
    # slurm.pc (pkgconf). If mpibind can't find
    # slurm's includedir, the plugin won't be built.
    # If slurm.pc is provided by slurm at some point,
    # uncomment the dependency below, otherwise,
    # make sure this works:
    #   pkg-config --variable=includedir slurm
    # depends_on("slurm", type="link",
    #            when="+slurm")


    def autoreconf(self, spec, prefix):
        autoreconf("--install", "--verbose", "--force")

    @when("+flux")
    def setup_run_environment(self, env: EnvironmentModifications) -> None:
        """Load the mpibind plugin into Flux"""
        env.prepend_path("FLUX_SHELL_RC_PATH", join_path(self.prefix, "share", "mpibind"))

    # To build and run the C unit tests, make sure 'libtap'
    # is installed and recognized by pkgconfig.
    # To build and run the Python unit tests, make sure 'pycotap'
    # is installed in your Python environment.
    # Unfortunately, 'tap' and 'pycotap' are not in Spack.
