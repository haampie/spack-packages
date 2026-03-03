from .generic import Package
class IntelOneApiPackage(Package):
    def update_description(cls):
        """Updates oneapi package descriptions with common text."""
        text = """ LICENSE INFORMATION: By downloading and using this software, you agree to the terms
        and conditions of the software license agreements at https://intel.ly/393CijO."""
        cls.__doc__ = cls.__doc__ + text
        return cls
        """Subdirectory for this component in the install prefix."""
        raise NotImplementedError
