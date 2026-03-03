from spack.package import (
    PackageBase,
    build_system,
    depends_on,
)
class AutotoolsPackage(PackageBase):
        depends_on("gmake", type="build")
