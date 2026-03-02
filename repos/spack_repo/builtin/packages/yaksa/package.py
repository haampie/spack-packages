# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.rocm import ROCmPackage

from spack.package import *


class Yaksa(AutotoolsPackage, CudaPackage, ROCmPackage):
    """Yaksa is a high-performance datatype engine for expressing,
    managing and manipulating data present in noncontiguous memory
    regions. It provides portable abstractions for structured
    noncontiguous data layouts that are much more comprehensive compared
    with traditional I/O vectors.

    Yaksa imitates parts of the MPI Datatype system, but adds additional
    functionality that would allow it to be used independent of MPI. It
    provides routines for packing/unpacking, creating I/O vectors (array
    of contiguous segments) and flattening/unflattening datatypes into
    process-portable formats.

    Yaksa's backend includes support for CPUs as well as different
    GPUs."""

    homepage = "https://www.yaksa.org"
    url = "https://github.com/pmodels/yaksa/archive/refs/tags/v0.2.tar.gz"




    depends_on("python@3:", type="build")

    # fix for error: no member named 'memoryType' in 'struct hipPointerAttribute_t'
    patch(
        "https://github.com/pmodels/yaksa/commit/5ebbadb7771d194f3819e3dd1ac8b5b467024afb.patch?full_index=1",
        sha256="0ae3ab6f932c1b31dde38babc181c1507e70d87e435d8fc6c82e0911fb55d560",
        when="@0.3 +rocm ^hip@6:",
    )

