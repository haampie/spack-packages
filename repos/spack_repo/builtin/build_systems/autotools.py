from spack.package import (
    PackageBase,
    build_system,
    depends_on,
    execute_install_time_tests,
    when,
    working_dir,
)
class AutotoolsPackage(PackageBase):
    build_system("autotools")
    with when("build_system=autotools"):
        depends_on("gmake", type="build")
