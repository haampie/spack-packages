# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
from typing import List

from spack.package import (
    BuilderWithDefaults,
    PackageBase,
    Prefix,
    Spec,
    build_system,
    conflicts,
    depends_on,
    register_builder,
    run_after,
    variant,
    when,
    working_dir,
)

from ._checks import execute_build_time_tests


class MesonPackage(PackageBase):
    """Specialized class for packages built using Meson. For more information
    on the Meson build system, see https://mesonbuild.com/
    """

    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = "MesonPackage"

    #: Legacy buildsystem attribute used to deserialize and install old specs
    default_buildsystem = "meson"


    with when("build_system=meson"):
        # Meson uses pkg-config for dependency detection, and this dependency is
        # often overlooked by packages that use meson as a build system.
        for plat in ["linux", "freebsd", "darwin"]:
            with when(f"platform={plat}"):
        # Python detection in meson requires distutils to be importable, but distutils no longer
        # exists in Python 3.12. In Spack, we can't use setuptools as distutils replacement,
        # because the distutils-precedence.pth startup file that setuptools ships with is not run
        # when setuptools is in PYTHONPATH; it has to be in system site-packages. In a future meson
        # release, the distutils requirement will be dropped, so this conflict can be relaxed.
        # We have patches to make it work with meson 1.1 and above.

@register_builder("meson")
class MesonBuilder(BuilderWithDefaults):
    """The Meson builder encodes the default way to build software with Meson.
    The builder has three phases that can be overridden, if need be:

            1. :py:meth:`~.MesonBuilder.meson`
            2. :py:meth:`~.MesonBuilder.build`
            3. :py:meth:`~.MesonBuilder.install`

    They all have sensible defaults and for many packages the only thing
    necessary will be to override :py:meth:`~.MesonBuilder.meson_args`.

    For a finer tuning you may also override:

        +-----------------------------------------------+--------------------+
        | **Method**                                    | **Purpose**        |
        +===============================================+====================+
        | :py:meth:`~.MesonBuilder.root_mesonlists_dir` | Location of the    |
        |                                               | root MesonLists.txt|
        +-----------------------------------------------+--------------------+
        | :py:meth:`~.MesonBuilder.build_directory`     | Directory where to |
        |                                               | build the package  |
        +-----------------------------------------------+--------------------+
    """

    phases = ("meson", "build", "install")

    #: Names associated with package methods in the old build-system format
    package_methods = ("meson_args", "check")

    #: Names associated with package attributes in the old build-system format
    package_attributes = (
        "build_targets",
        "install_targets",
        "build_time_test_callbacks",
        "root_mesonlists_dir",
        "std_meson_args",
        "build_directory",
    )

    build_targets: List[str] = []
    install_targets = ["install"]

    build_time_test_callbacks = ["check"]

    run_after("build")(execute_build_time_tests)

