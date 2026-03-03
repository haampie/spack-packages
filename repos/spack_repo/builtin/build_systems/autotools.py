from spack.package import (
    PackageBase,
    depends_on,
)
class AutotoolsPackage(PackageBase):
        depends_on("gmake", type="build")
