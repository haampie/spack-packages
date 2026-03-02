import os
import re
from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.gnu import GNUMirrorPackage
from spack.package import *
class M4(AutotoolsPackage, GNUMirrorPackage):
    version("1.4.21", sha256="38ae59f7a30bf9c108193cc5c25fbb06014f21e230c7ede2eff614f7b7c37ed8")
    version("1.4.20", sha256="6ac4fc31ce440debe63987c2ebbf9d7b6634e67a7c3279257dc7361de8bdb3ef")
    depends_on("c", type="build")  # generated
    executables = ["^g?m4$"]
