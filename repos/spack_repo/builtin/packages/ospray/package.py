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


    variant("apps", default=False, description="Enable building OSPRay Apps")
    variant("denoiser", default=True, description="Enable denoiser image operation")
    variant("glm", default=False, description="Build ospray_cpp GLM tests/tutorial")
    variant("mpi", default=True, description="Enable MPI support")
    variant("volumes", default=True, description="Enable volumetric rendering with Open VKL")



    with when("+volumes"):
        depends_on("openvkl@2:", when="@3:")
        depends_on("openvkl@2.0.1:", when="@3.2:")
    with when("+denoiser"):
        depends_on("openimagedenoise@1.2.3:")
        depends_on("openimagedenoise@1.3:", when="@2.5:")
        depends_on("openimagedenoise@:1", when="@:2.11")
        depends_on("openimagedenoise@2:", when="@2.12:")
        depends_on("openimagedenoise@2.1:", when="@3:")
        depends_on("openimagedenoise@2.3:", when="@3.2:")
    depends_on("ispc@1.14.1:", type=("build"))
    depends_on("ispc@1.16.0:", when="@2.7.0:", type=("build"))
    depends_on("ispc@1.18.0:", when="@2.10.0:", type=("build"))
    depends_on("ispc@1.19.0:", when="@2.11.0:", type=("build"))
    depends_on("ispc@1.20.0:", when="@2.12.0:", type=("build"))
    depends_on("ispc@1.21.1:", when="@3:", type=("build"))
    depends_on("ispc@1.23.0:", when="@3.2:", type=("build"))
    depends_on("tbb")

    with when("+mpi"):
        depends_on("mpi")
        depends_on("snappy@1.1.8:")
        depends_on("snappy@1.2.1:", when="@3.2:")

