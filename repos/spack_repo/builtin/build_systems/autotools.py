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

    def check(self) -> None:
        """Run "make" on the ``test`` and ``check`` targets, if found."""
        with working_dir(self.build_directory):
            self.pkg._if_make_target_execute("test")
            self.pkg._if_make_target_execute("check")

    def _activate_or_not(
        self,
        name: str,
        activation_word: str,
        deactivation_word: str,
        activation_value: Optional[Union[Callable, str]] = None,
        variant=None,
    ) -> List[str]:
        """This function contain the current implementation details of
        :meth:`~spack_repo.builtin.build_systems.autotools.AutotoolsBuilder.with_or_without` and
        :meth:`~spack_repo.builtin.build_systems.autotools.AutotoolsBuilder.enable_or_disable`.

        Args:
            name: name of the option that is being activated or not
            activation_word: the default activation word ('with' in the case of
                ``with_or_without``)
            deactivation_word: the default deactivation word ('without' in the case of
                ``with_or_without``)
            activation_value: callable that accepts a single value. This value is either one of the
                allowed values for a multi-valued variant or the name of a bool-valued variant.
                Returns the parameter to be used when the value is activated.

                The special value "prefix" can also be assigned and will return
                ``spec[name].prefix`` as activation parameter.
            variant: name of the variant that is being processed (if different from option name)

        Examples:

            Given a package with:

            .. code-block:: python

                variant("foo", values=("x", "y"), description=")
                variant("bar", default=True, description=")
                variant("ba_z", default=True, description=")

            calling this function like:

            .. code-block:: python

                _activate_or_not(
                    "foo", "with", "without", activation_value="prefix"
                )
                _activate_or_not("bar", "with", "without")
                _activate_or_not("ba-z", "with", "without", variant="ba_z")

            will generate the following configuration options:

            .. code-block:: console

                --with-x=<prefix-to-x> --without-y --with-bar --with-ba-z

            for ``<spec-name> foo=x +bar``

        Note: returns an empty list when the variant is conditional and its condition
              is not met.

        Returns:
            list: list of strings that corresponds to the activation/deactivation
            of the variant that has been processed

        Raises:
            KeyError: if name is not among known variants
        """
        spec: Spec = self.pkg.spec
        args: List[str] = []

        if activation_value == "prefix":
            activation_value = lambda x: spec[x].prefix

        variant = variant or name

        # Defensively look that the name passed as argument is among variants
        if not self.pkg.has_variant(variant):
            msg = '"{0}" is not a variant of "{1}"'
            raise KeyError(msg.format(variant, self.pkg.name))

        if variant not in spec.variants:
            return []

        # Create a list of pairs. Each pair includes a configuration
        # option and whether or not that option is activated
        vdef = self.pkg.get_variant(variant)
        if set(vdef.values) == set((True, False)):  # type: ignore
            # BoolValuedVariant carry information about a single option.
            # Nonetheless, for uniformity of treatment we'll package them
            # in an iterable of one element.
            options = [(name, f"+{variant}" in spec)]
        else:
            # "feature_values" is used to track values which correspond to
            # features which can be enabled or disabled as understood by the
            # package's build system. It excludes values which have special
            # meanings and do not correspond to features (e.g. "none")
            feature_values = getattr(vdef.values, "feature_values", None) or vdef.values
            options = [(v, f"{variant}={v}" in spec) for v in feature_values]  # type: ignore

        # For each allowed value in the list of values
        for option_value, activated in options:
            # Search for an override in the package for this value
            override_name = f"{activation_word}_or_{deactivation_word}_{option_value}"
            line_generator = getattr(self, override_name, None) or getattr(
                self.pkg, override_name, None
            )
            # If not available use a sensible default
            if line_generator is None:

                def _default_generator(is_activated):
                    if is_activated:
                        line = f"--{activation_word}-{option_value}"
                        if activation_value is not None and activation_value(option_value):
                            line = f"{line}={activation_value(option_value)}"
                        return line
                    return f"--{deactivation_word}-{option_value}"

                line_generator = _default_generator
            args.append(line_generator(activated))
        return args

    def with_or_without(
        self,
        name: str,
        activation_value: Optional[Union[Callable, str]] = None,
        variant: Optional[str] = None,
    ) -> List[str]:
        """Inspects a variant and returns the arguments that activate
        or deactivate the selected feature(s) for the configure options.

        This function works on all type of variants. For bool-valued variants
        it will return by default ``--with-{name}`` or ``--without-{name}``.
        For other kinds of variants it will cycle over the allowed values and
        return either ``--with-{value}`` or ``--without-{value}``.

        If activation_value is given, then for each possible value of the
        variant, the option ``--with-{value}=activation_value(value)`` or
        ``--without-{value}`` will be added depending on whether or not
        ``variant=value`` is in the spec.

        Args:
            name: name of a valid multi-valued variant
            activation_value: callable that accepts a single value and returns the parameter to be
                used leading to an entry of the type ``--with-{name}={parameter}``.

                The special value "prefix" can also be assigned and will return
                ``spec[name].prefix`` as activation parameter.

        Returns:
            list of arguments to configure
        """
        return self._activate_or_not(name, "with", "without", activation_value, variant)

    def enable_or_disable(
        self,
        name: str,
        activation_value: Optional[Union[Callable, str]] = None,
        variant: Optional[str] = None,
    ) -> List[str]:
        """Same as
        :meth:`~spack_repo.builtin.build_systems.autotools.AutotoolsBuilder.with_or_without`
        but substitute ``with`` with ``enable`` and ``without`` with ``disable``.

        Args:
            name: name of a valid multi-valued variant
            activation_value: if present accepts a single value and returns the parameter to be
                used leading to an entry of the type ``--enable-{name}={parameter}``

                The special value "prefix" can also be assigned and will return
                ``spec[name].prefix`` as activation parameter.

        Returns:
            list of arguments to configure
        """
        return self._activate_or_not(name, "enable", "disable", activation_value, variant)


    def installcheck(self) -> None:
        """Run "make" on the ``installcheck`` target, if found."""
        with working_dir(self.build_directory):
            self.pkg._if_make_target_execute("installcheck")

    @run_after("install")
    def _remove_libtool_archives(self) -> None:
        """Remove all .la files in prefix sub-folders if the package sets
        ``install_libtool_archives`` to be False.
        """
        # If .la files are to be installed there's nothing to do
        if self.install_libtool_archives:
            return

        # Remove the files and create a log of what was removed
        libtool_files = find(str(self.pkg.prefix), "*.la", recursive=True)
        with safe_remove(*libtool_files):
            mkdirp(os.path.dirname(self._removed_la_files_log))
            with open(self._removed_la_files_log, mode="w", encoding="utf-8") as f:
                f.write("\n".join(libtool_files))

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        if self.spec.platform == "darwin" and macos_version() >= Version("11"):
            # Many configure files rely on matching '10.*' for macOS version
            # detection and fail to add flags if it shows as version 11.
            env.set("MACOSX_DEPLOYMENT_TARGET", "10.16")

    # On macOS, force rpaths for shared library IDs and remove duplicate rpaths
    run_after("install", when="platform=darwin")(apply_macos_rpath_fixups)


def _autoreconf_search_path_args(spec: Spec) -> List[str]:
    dirs_seen: Set[Tuple[int, int]] = set()
    flags_spack: List[str] = []
    flags_external: List[str] = []

    # We don't want to add an include flag for automake's default search path.
    for automake in spec.dependencies(name="automake", deptype="build"):
        try:
            s = os.stat(automake.prefix.share.aclocal)
            if stat.S_ISDIR(s.st_mode):
                dirs_seen.add((s.st_ino, s.st_dev))
        except OSError:
            pass

    for dep in spec.dependencies(deptype="build"):
        path = dep.prefix.share.aclocal
        # Skip non-existing aclocal paths
        try:
            s = os.stat(path)
        except OSError:
            continue
        # Skip things seen before, as well as non-dirs.
        if (s.st_ino, s.st_dev) in dirs_seen or not stat.S_ISDIR(s.st_mode):
            continue
        dirs_seen.add((s.st_ino, s.st_dev))
        flags = flags_external if dep.external else flags_spack
        flags.extend(["-I", path])
    return flags_spack + flags_external
