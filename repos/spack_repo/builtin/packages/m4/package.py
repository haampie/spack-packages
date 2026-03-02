from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.gnu import GNUMirrorPackage
from spack.package import *
class M4(AutotoolsPackage, GNUMirrorPackage):
    version("1.4.17", sha256="3ce725133ee552b8b4baca7837fb772940b25e81b2a9dc92537aeaf733538c9e")
    depends_on("c", type="build")  # generated
