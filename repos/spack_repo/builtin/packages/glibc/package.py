from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.gnu import GNUMirrorPackage
from spack.package import *
class Glibc(AutotoolsPackage, GNUMirrorPackage):
    git = "https://sourceware.org/git/glibc.git"
    build_directory = "build"
    tags = ["runtime"]
    provides("libc")
