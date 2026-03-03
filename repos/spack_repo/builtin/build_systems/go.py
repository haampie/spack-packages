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
    depends_on,
    execute_install_time_tests,
    install,
    join_path,
    mkdirp,
    register_builder,
    run_after,
    when,
    working_dir,
)


class GoPackage(PackageBase):
    """Specialized class for packages built using the Go toolchain."""

    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = "GoPackage"

    #: Legacy buildsystem attribute used to deserialize and install old specs
    default_buildsystem = "go"

    build_system("go")

    with when("build_system=go"):
        depends_on("go", type="build")


@register_builder("go")
class GoBuilder(BuilderWithDefaults):
    """The Go builder encodes the most common way of building software with
    a golang go.mod file. It has two phases that can be overridden, if need be:

            1. :py:meth:`~.GoBuilder.build`
            2. :py:meth:`~.GoBuilder.install`

    For a finer tuning you may override:

        +-----------------------------------------------+--------------------+
        | **Method**                                    | **Purpose**        |
        +===============================================+====================+
        | :py:attr:`~.GoBuilder.build_args`             | Specify arguments  |
        |                                               | to ``go build``    |
        +-----------------------------------------------+--------------------+
        | :py:attr:`~.GoBuilder.check_args`             | Specify arguments  |
        |                                               | to ``go test``     |
        +-----------------------------------------------+--------------------+
    """

    phases = ("build", "install")

    #: Names associated with package methods in the old build-system format
    package_methods = ("check", "installcheck")

    #: Names associated with package attributes in the old build-system format
    package_attributes = (
        "build_args",
        "check_args",
        "build_directory",
        "install_time_test_callbacks",
        "cgo_enabled",
    )

    #: Callback names for install-time test
    install_time_test_callbacks = ["check"]

    # Enable or Disable CGO functionality in builds. (Disabled by default)
    cgo_enabled = False

    run_after("install")(execute_install_time_tests)

