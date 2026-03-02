from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.gnu import GNUMirrorPackage
from spack.package import *
class Glibc(AutotoolsPackage, GNUMirrorPackage):
    provides("libc")
