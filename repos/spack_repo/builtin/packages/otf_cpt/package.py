# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class OtfCpt(CMakePackage):
    """Tool to collect and report model factors (aka. fundamental performance factors)
    for hybrid MPI + OpenMP applications on-the-fly."""

    # Add a proper url for your package's homepage here.
    homepage = (
        "https://github.com/RWTH-HPC/OTF-CPT?tab=readme-ov-file#on-the-fly-critical-path-tool"
    )
    git = "https://github.com/RWTH-HPC/OTF-CPT.git"

    maintainers("jgraciahlrs", "jprotze")

    license("Apache-2.0", checked_by="jgraciahlrs")

    version("0.9", tag="v0.9")

    depends_on("cxx", type="build")

