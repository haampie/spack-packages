from spack.package import (
    BuilderWithDefaults,
    EnvironmentModifications,
    Executable,
    FileFilter,
    InstallError,
    ModuleChangePropagator,
    PackageBase,
    Prefix,
    when,
    working_dir,
)
from ._checks import ensure_build_dependencies_or_raise, execute_build_time_tests
class AutotoolsPackage(PackageBase):
    """Specialized class for packages built using GNU Autotools."""
    #: This attribute is used in UI queries that need to know the build
