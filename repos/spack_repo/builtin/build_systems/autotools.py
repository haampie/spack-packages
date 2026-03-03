# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import stat
import subprocess
from typing import Callable, List, Optional, Set, Tuple, Union

from spack.package import (
    BuilderWithDefaults,
    EnvironmentModifications,
    Executable,
    FileFilter,
    InstallError,
    ModuleChangePropagator,
    PackageBase,
    Prefix,
    Spec,
    Version,
    apply_macos_rpath_fixups,
    build_system,
    compiler_spec,
    conflicts,
    copy,
    create_builder,
    depends_on,
    execute_install_time_tests,
    find,
    force_remove,
    is_exe,
    keep_modification_time,
    macos_version,
    mkdirp,
    register_builder,
    run_after,
    run_before,
    safe_remove,
    tty,
    when,
    working_dir,
)

from ._checks import ensure_build_dependencies_or_raise, execute_build_time_tests


class AutotoolsPackage(PackageBase):
    """Specialized class for packages built using GNU Autotools."""

    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = "AutotoolsPackage"

    #: Legacy buildsystem attribute used to deserialize and install old specs
    default_buildsystem = "autotools"

    build_system("autotools")

    with when("build_system=autotools"):
        depends_on("gnuconfig", type="build", when="target=ppc64le:")
        depends_on("gnuconfig", type="build", when="target=aarch64:")
        depends_on("gnuconfig", type="build", when="target=riscv64:")
        depends_on("gmake", type="build")

    # Legacy methods (used by too many packages to change them,
    # need to forward to the builder)
@register_builder("autotools")
class AutotoolsBuilder(BuilderWithDefaults):
    """The autotools builder encodes the default way of installing software built
    with autotools. It has four phases that can be overridden, if need be:

        1. :py:meth:`~.AutotoolsBuilder.autoreconf`
        2. :py:meth:`~.AutotoolsBuilder.configure`
        3. :py:meth:`~.AutotoolsBuilder.build`
        4. :py:meth:`~.AutotoolsBuilder.install`

    They all have sensible defaults and for many packages the only thing necessary
    is to override the helper method
    :meth:`~spack_repo.builtin.build_systems.autotools.AutotoolsBuilder.configure_args`.

    For a finer tuning you may also override:

        +-----------------------------------------------+--------------------+
        | **Method**                                    | **Purpose**        |
        +===============================================+====================+
        | :py:attr:`~.AutotoolsBuilder.build_targets`   | Specify ``make``   |
        |                                               | targets for the    |
        |                                               | build phase        |
        +-----------------------------------------------+--------------------+
        | :py:attr:`~.AutotoolsBuilder.install_targets` | Specify ``make``   |
        |                                               | targets for the    |
        |                                               | install phase      |
        +-----------------------------------------------+--------------------+
        | :py:meth:`~.AutotoolsBuilder.check`           | Run  build time    |
        |                                               | tests if required  |
        +-----------------------------------------------+--------------------+

    """

    #: Phases of a GNU Autotools package
    phases = ("autoreconf", "configure", "build", "install")

    #: Names associated with package methods in the old build-system format
    package_methods = ("configure_args", "check", "installcheck")

    #: Names associated with package attributes in the old build-system format
    package_attributes = (
        "archive_files",
        "patch_libtool",
        "build_targets",
        "install_targets",
        "build_time_test_callbacks",
        "install_time_test_callbacks",
        "force_autoreconf",
        "autoreconf_extra_args",
        "install_libtool_archives",
        "patch_config_files",
        "configure_directory",
        "configure_abs_path",
        "build_directory",
        "autoreconf_search_path_args",
    )

    #: Whether to update ``libtool`` (e.g. for Arm/Clang/Fujitsu/NVHPC compilers)
    patch_libtool = True

    #: Targets for ``make`` during the :py:meth:`~.AutotoolsBuilder.build` phase
    build_targets: List[str] = []
    #: Targets for ``make`` during the :py:meth:`~.AutotoolsBuilder.install` phase
    install_targets = ["install"]

    #: Callback names for build-time test
    build_time_test_callbacks = ["check"]

    #: Callback names for install-time test
    install_time_test_callbacks = ["installcheck"]

    #: Set to true to force the autoreconf step even if configure is present
    force_autoreconf = False

    #: Options to be passed to autoreconf when using the default implementation
    autoreconf_extra_args: List[str] = []

    #: If False deletes all the .la files in the prefix folder after the installation.
    #: If True instead it installs them.
    install_libtool_archives = False



    # On macOS, force rpaths for shared library IDs and remove duplicate rpaths


