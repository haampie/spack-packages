# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import re

from spack.package import (
    BuilderWithDefaults,
    Executable,
    PackageBase,
    Prefix,
    Spec,
    build_system,
    depends_on,
    execute_install_time_tests,
    extends,
    find,
    register_builder,
    run_after,
    test_part,
    tty,
    when,
    working_dir,
)


class SIPPackage(PackageBase):
    """Specialized class for packages that are built using the
    SIP build system. See https://www.riverbankcomputing.com/software/sip/intro
    for more information.
    """

    # To be used in UI queries that require to know which
    # build-system class we are using
    build_system_class = "SIPPackage"

    #: Name of private sip module to install alongside package
    sip_module = "sip"

    #: Callback names for install-time testing
    install_time_test_callbacks = ["test_imports"]
    #: Legacy buildsystem attribute used to deserialize and install old specs
    default_buildsystem = "sip"

    build_system("sip")

    with when("build_system=sip"):
        extends("python", type=("build", "link", "run"))

@register_builder("sip")
class SIPBuilder(BuilderWithDefaults):
    """The SIP builder provides the following phases that can be overridden:

    * configure
    * build
    * install

    The configure phase already adds a set of default flags. To see more
    options, run ``sip-build --help``.
    """

    phases = ("configure", "build", "install")

    #: Names associated with package methods in the old build-system format
    package_methods = ("configure_args", "build_args", "install_args")

    #: Names associated with package attributes in the old build-system format
    package_attributes = (
        "build_targets",
        "install_targets",
        "build_time_test_callbacks",
        "install_time_test_callbacks",
        "build_directory",
    )

    build_directory = "build"

    run_after("install")(execute_install_time_tests)
