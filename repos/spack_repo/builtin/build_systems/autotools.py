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
    #: system base class
class AutotoolsBuilder(BuilderWithDefaults):
    """The autotools builder encodes the default way of installing software built
    with autotools. It has four phases that can be overridden, if need be:
        1. :py:meth:`~.AutotoolsBuilder.autoreconf`
        2. :py:meth:`~.AutotoolsBuilder.configure`
        3. :py:meth:`~.AutotoolsBuilder.build`
    """
    #: Phases of a GNU Autotools package
