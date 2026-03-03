# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import (
    BuilderWithDefaults,
    PackageBase,
    Prefix,
    Spec,
    build_system,
    depends_on,
    execute_install_time_tests,
    register_builder,
    run_after,
    working_dir,
)

from ._checks import execute_build_time_tests


class WafPackage(PackageBase):
    """Specialized class for packages that are built using the
    Waf build system. See https://waf.io/book/ for more information.
    """

    # To be used in UI queries that require to know which
    # build-system class we are using
    build_system_class = "WafPackage"
    #: Legacy buildsystem attribute used to deserialize and install old specs
    default_buildsystem = "waf"

    build_system("waf")
    # Much like AutotoolsPackage does not require automake and autoconf
    # to build, WafPackage does not require waf to build. It only requires
    # python to run the waf build script.


@register_builder("waf")
class WafBuilder(BuilderWithDefaults):
    """The WAF builder provides the following phases that can be overridden:

    * configure
    * build
    * install

    These are all standard Waf commands and can be found by running:

    .. code-block:: console

       $ python waf --help

    Each phase provides a function <phase> that runs:

    .. code-block:: console

       $ python waf -j<jobs> <phase>

    where <jobs> is the number of parallel jobs to build with. Each phase
    also has a <phase_args> function that can pass arguments to this call.
    All of these functions are empty except for the ``configure_args``
    function, which passes ``--prefix=/path/to/installation/prefix``.
    """

    phases = ("configure", "build", "install")

    #: Names associated with package methods in the old build-system format
    package_methods = (
        "build_test",
        "install_test",
        "configure_args",
        "build_args",
        "install_args",
        "build_test",
        "install_test",
    )

    #: Names associated with package attributes in the old build-system format
    package_attributes = (
        "build_time_test_callbacks",
        "build_directory",
        "install_time_test_callbacks",
    )

    # Callback names for build-time test
    build_time_test_callbacks = ["build_test"]

    # Callback names for install-time test
    install_time_test_callbacks = ["install_test"]

    run_after("build")(execute_build_time_tests)

    run_after("install")(execute_install_time_tests)
