from spack_repo.builtin.build_systems.compiler import CompilerPackage
from spack_repo.builtin.build_systems.oneapi import IntelOneApiPackage
from spack.package import *
class IntelOneapiCompilers(IntelOneApiPackage, CompilerPackage):
    provides("c", "cxx")
