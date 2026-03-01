from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *
class JsonC(CMakePackage):
    version("0.15", sha256="b8d80a1ddb718b3ba7492916237bbf86609e9709fb007e7f7d4322f02341a4c6")
    depends_on("c", type="build")
