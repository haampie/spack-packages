# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import glob

from spack.package import (
    BuilderWithDefaults,
    PackageBase,
    Prefix,
    Spec,
    build_system,
    extends,
    maintainers,
    register_builder,
)


class RubyPackage(PackageBase):
    """Specialized class for building Ruby gems."""


    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = "RubyPackage"
    #: Legacy buildsystem attribute used to deserialize and install old specs
    default_buildsystem = "ruby"

    build_system("ruby")

    extends("ruby", when="build_system=ruby")


@register_builder("ruby")
class RubyBuilder(BuilderWithDefaults):
    """The Ruby builder provides two phases that can be overridden if required:

    #. :py:meth:`~.RubyBuilder.build`
    #. :py:meth:`~.RubyBuilder.install`
    """

    phases = ("build", "install")

    #: Names associated with package methods in the old build-system format
    package_methods = ()

    #: Names associated with package attributes in the old build-system format
    package_attributes = ()

