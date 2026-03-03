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
        depends_on("gnuconfig", type="build", when="target=riscv64:")
        depends_on("gmake", type="build")
    # Legacy methods (used by too many packages to change them,
    # need to forward to the builder)
