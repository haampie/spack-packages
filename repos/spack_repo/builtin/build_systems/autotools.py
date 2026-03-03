from spack.package import (
    BuilderWithDefaults,
    EnvironmentModifications,
    Executable,
    FileFilter,
    InstallError,
    ModuleChangePropagator,
    PackageBase,
    Prefix,
    Spec,
    Version,
    apply_macos_rpath_fixups,
    build_system,
    compiler_spec,
    conflicts,
    copy,
    create_builder,
    depends_on,
    execute_install_time_tests,
    find,
    force_remove,
    safe_remove,
    tty,
    when,
    working_dir,
)
from ._checks import ensure_build_dependencies_or_raise, execute_build_time_tests
class AutotoolsPackage(PackageBase):
    """Specialized class for packages built using GNU Autotools."""
    #: This attribute is used in UI queries that need to know the build
    build_system("autotools")
    with when("build_system=autotools"):
        depends_on("gnuconfig", type="build", when="target=riscv64:")
        depends_on("gmake", type="build")
