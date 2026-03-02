from spack.package import (
    EnvironmentModifications,
    Executable,
    variant,
)
from .generic import Package
class IntelOneApiPackage(Package):
    """Base class for Intel oneAPI packages."""
    homepage = "https://software.intel.com/oneapi"
    variant("envmods", default=True, description="Toggles environment modifications")
    @staticmethod
    def update_description(cls):
        return cls
class IntelOneApiLibraryPackage(IntelOneApiPackage):
    """Base class for Intel oneAPI library packages.
    Contains some convenient default implementations for libraries.
    Implement the method directly in the package if something
    different is needed.
    """
    # HFP: for the time being, this package queries
    # - compiler for its library path
