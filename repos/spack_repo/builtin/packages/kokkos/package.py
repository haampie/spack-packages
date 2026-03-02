from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.rocm import ROCmPackage
class Kokkos(CMakePackage, CudaPackage, ROCmPackage):
    homepage = "https://github.com/kokkos/kokkos"
