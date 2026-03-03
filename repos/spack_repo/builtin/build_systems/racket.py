# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
from typing import Optional, Tuple

from spack.package import (
    Builder,
    ClassProperty,
    Executable,
    PackageBase,
    Prefix,
    ProcessError,
    Spec,
    build_system,
    classproperty,
    determine_number_of_jobs,
    extends,
    maintainers,
    register_builder,
    tty,
    working_dir,
)


class RacketPackage(PackageBase):
    """Specialized class for packages that are built using Racket's
    `raco pkg install` and `raco setup` commands.
    """

    #: Package name, version, and extension on PyPI
    # To be used in UI queries that require to know which
    # build-system class we are using
    build_system_class = "RacketPackage"
    #: Legacy buildsystem attribute used to deserialize and install old specs
    default_buildsystem = "racket"

    build_system("racket")

    extends("racket", when="build_system=racket")

    racket_name: Optional[str] = None
    homepage: ClassProperty[Optional[str]] = classproperty(_homepage)


@register_builder("racket")
class RacketBuilder(Builder):
    """The Racket builder provides an ``install`` phase that can be overridden."""

    phases = ("install",)

    #: Names associated with package methods in the old build-system format
    package_methods: Tuple[str, ...] = tuple()

    #: Names associated with package attributes in the old build-system format
    package_attributes = ("build_directory", "build_time_test_callbacks", "subdirectory")

    #: Callback names for build-time test
    build_time_test_callbacks = ["check"]

    racket_name: Optional[str] = None

