# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import List  # novm

from spack.package import (
    BuilderWithDefaults,
    PackageBase,
    Prefix,
    Spec,
    build_system,
    conflicts,
    register_builder,
    windows_sfn,
    working_dir,
)


class NMakePackage(PackageBase):
    """Specialized class for packages built using a Makefiles."""

    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = "NMakePackage"

    build_system("nmake")


@register_builder("nmake")
class NMakeBuilder(BuilderWithDefaults):
    """The NMake builder encodes the most common way of building software with
    Mircosoft's NMake tool. It has two phases that can be overridden, if need be:

            1. :py:meth:`~.NMakeBuilder.build`
            2. :py:meth:`~.NMakeBuilder.install`

    It is usually necessary to override the :py:meth:`~.NMakeBuilder.install`
    phase as many packages with NMake systems neglect to provide an install
    target. The default install phase will attempt to invoke an install target
    from NMake. If none exists, this will result in a build failure

    For a finer tuning you may override:

        +-----------------------------------------------+---------------------+
        | **Method**                                    | **Purpose**         |
        +===============================================+=====================+
        | :py:attr:`~.NMakeBuilder.build_targets`       | Specify ``nmake``   |
        |                                               | targets for the     |
        |                                               | build phase         |
        +-----------------------------------------------+---------------------+
        | :py:attr:`~.NMakeBuilder.install_targets`     | Specify ``nmake``   |
        |                                               | targets for the     |
        |                                               | install phase       |
        +-----------------------------------------------+---------------------+
        | :py:meth:`~.NMakeBuilder.build_directory`     | Directory where the |
        |                                               | project makefile    |
        |                                               | is located          |
        +-----------------------------------------------+---------------------+
    """

    phases = ("build", "install")

    #: Targets for ``make`` during the :py:meth:`~.NMakeBuilder.build` phase
    build_targets: List[str] = []
    #: Targets for ``make`` during the :py:meth:`~.NMakeBuilder.install` phase
    install_targets: List[str] = ["INSTALL"]

