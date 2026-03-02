from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.gnu import GNUMirrorPackage
from spack.package import *
class M4(AutotoolsPackage, GNUMirrorPackage):
    version("1.4.20", sha256="6ac4fc31ce440debe63987c2ebbf9d7b6634e67a7c3279257dc7361de8bdb3ef")
    depends_on("c", type="build")  # generated
    executables = ["^g?m4$"]
