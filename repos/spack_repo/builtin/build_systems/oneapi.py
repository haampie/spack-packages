from .generic import Package
class IntelOneApiPackage(Package):
    """Base class for Intel oneAPI packages."""
    homepage = "https://software.intel.com/oneapi"
    # oneAPI license does not allow mirroring outside of the
    # organization (e.g. University/Company).
    # contains precompiled binaries without rpaths
    unresolved_libraries = ["*"]
    def update_description(cls):
        """Updates oneapi package descriptions with common text."""
        text = """ LICENSE INFORMATION: By downloading and using this software, you agree to the terms
        and conditions of the software license agreements at https://intel.ly/393CijO."""
        cls.__doc__ = cls.__doc__ + text
        return cls
    @property
    def component_dir(self):
        """Subdirectory for this component in the install prefix."""
        raise NotImplementedError
