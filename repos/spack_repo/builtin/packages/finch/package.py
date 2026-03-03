# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.rocm import ROCmPackage

from spack.package import *

from ..kokkos.package import Kokkos


class Finch(CMakePackage, CudaPackage, ROCmPackage):
    """Heat transfer for additive manufacturing with Cabana"""

    homepage = "https://github.com/ORNL-MDF/Finch"
    git = "https://github.com/ORNL-MDF/Finch.git"
    url = "https://github.com/ORNL-MDF/Finch/archive/0.2.0.tar.gz"


    version("0.1.0", sha256="d74612916dcaa8121bac9f0f14b3da665841d82744176c780b3b824503b81430")

    _kokkos_backends = Kokkos.devices_variants
    for _backend in _kokkos_backends:
        _deflt, _descr = _kokkos_backends[_backend]
        variant(_backend.lower(), default=_deflt, description=_descr)

    variant("shared", default=True, description="Build shared libraries")


    for _backend in _kokkos_backends:
        # Handled separately below
        if _backend != "cuda" and _backend != "rocm":
            _backend_dep = "+{0}".format(_backend)

    for arch in CudaPackage.cuda_arch_values:
        cuda_dep = "+cuda cuda_arch={0}".format(arch)
    for arch in ROCmPackage.amdgpu_targets:
        rocm_dep = "+rocm amdgpu_target={0}".format(arch)

    def cmake_args(self):
        return [self.define_from_variant("BUILD_SHARED_LIBS", "shared")]
