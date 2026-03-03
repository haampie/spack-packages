# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import (
    BuilderWithDefaults,
    EnvironmentModifications,
    PackageBase,
    Prefix,
    Spec,
    build_system,
    extends,
    register_builder,
    when,
)


class OctavePackage(PackageBase):
    """Specialized class for Octave packages. See
    https://www.gnu.org/software/octave/doc/v4.2.0/Installing-and-Removing-Packages.html
    for more information.
    """

    # To be used in UI queries that require to know which
    # build-system class we are using
    build_system_class = "OctavePackage"
    #: Legacy buildsystem attribute used to deserialize and install old specs
    default_buildsystem = "octave"

    build_system("octave")

    with when("build_system=octave"):
        extends("octave")


@register_builder("octave")
class OctaveBuilder(BuilderWithDefaults):
    """The octave builder provides the following phases that can be overridden:

    1. :py:meth:`~.OctaveBuilder.install`
    """

    phases = ("install",)

    #: Names associated with package methods in the old build-system format
    package_methods = ()

    #: Names associated with package attributes in the old build-system format
    package_attributes = ()

