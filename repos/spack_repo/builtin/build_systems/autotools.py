from spack.package import (
    PackageBase,
    build_system,
    depends_on,
    execute_install_time_tests,
    when,
    working_dir,
)
class AutotoolsPackage(PackageBase):
        depends_on("gmake", type="build")
