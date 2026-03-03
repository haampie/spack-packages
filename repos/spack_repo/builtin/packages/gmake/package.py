from spack_repo.builtin.build_systems.gnu import GNUMirrorPackage
from spack.package import *
class Gmake(Package, GNUMirrorPackage):
    version("4.4.1", sha256="dd16fb1d67bfab79a72f5e8390735c49e3e8e70b4945a15ab1f81ddb78658fb3")
    variant("guile", default=False, description="Support GNU Guile for embedded scripting")
    depends_on("c", type="build")
