# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Ospray(CMakePackage):
    """Intel OSPRay is an open source, scalable, and portable ray tracing engine for
    high-performance, high-fidelity visualization on Intel Architecture CPUs."""

    homepage = "https://www.ospray.org/"
    url = "https://github.com/RenderKit/ospray/archive/v2.10.0.tar.gz"
    git = "https://github.com/RenderKit/ospray.git"

    # maintainers("aumuell")


    variant("denoiser", default=True, description="Enable denoiser image operation")
    variant("glm", default=False, description="Build ospray_cpp GLM tests/tutorial")
    variant("mpi", default=True, description="Enable MPI support")
    variant("volumes", default=True, description="Enable volumetric rendering with Open VKL")



    with when("+volumes"):
        depends_on("openvkl@2.0.1:", when="@3.2:")
    with when("+denoiser"):
        depends_on("openimagedenoise@1.2.3:")
        depends_on("openimagedenoise@1.3:", when="@2.5:")
