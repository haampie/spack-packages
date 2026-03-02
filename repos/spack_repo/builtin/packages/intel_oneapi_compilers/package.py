from spack_repo.builtin.build_systems.compiler import CompilerPackage
from spack_repo.builtin.build_systems.oneapi import IntelOneApiPackage
from spack.package import *
versions = [
    {
        "version": "2025.3.2",
        "cpp": {
        },
        "cpp": {
        },
    },
]
class IntelOneapiCompilers(IntelOneApiPackage, CompilerPackage):
    provides("c", "cxx")
    for v in versions:
        version(v["version"], expand=False, **v["cpp"])
