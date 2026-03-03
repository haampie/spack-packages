# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import sys

from spack_repo.builtin.build_systems import autotools, cmake, meson
from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.build_systems.meson import MesonPackage

from spack.package import *

IS_WINDOWS = sys.platform == "win32"


class Harfbuzz(MesonPackage, AutotoolsPackage, CMakePackage):
    """The Harfbuzz package contains an OpenType text shaping engine."""

    homepage = "https://github.com/harfbuzz/harfbuzz"
    url = "https://github.com/harfbuzz/harfbuzz/releases/download/9.0.0/harfbuzz-9.0.0.tar.xz"
    git = "https://github.com/harfbuzz/harfbuzz.git"

    build_system(
        conditional("autotools", when="@:2.9"),
        conditional("meson", when="@3:"),
        conditional("cmake", when="@10:"),
        default="meson" if not IS_WINDOWS else "cmake",
    )

    # HarfBuzz is licensed under the so-called "Old MIT" license,
    # for which no SPDX identifier is listed at https://spdx.org/licenses/
    # Ref: https://github.com/harfbuzz/harfbuzz/blob/main/COPYING
    license("MIT-old", checked_by="wdconinc")


    version("11.5.1", sha256="972a60a8d274d49e70361da6920c3a73dfb0fb4387f6c6811906a47ba634d8a1")
    variant("graphite2", default=False, description="enable support for graphite2 font engine")
    variant(
        "coretext",
        default=False,
        when="platform=darwin",
        description="Enable CoreText shaper backend on macOS",
    )
    variant("shared", default=True, when="build_system=cmake", description="Build shared harfbuzz")

    with when("build_system=cmake"):
        with when("platform=windows"):
            variant(
                "uniscribe",
                default=False,
                description="Enable Uniscribe shaper backend on Windows",
            )
            variant(
                "directwrite",
                default=False,
                description="Enable directwrite shaper backend on Windows",
            )
            variant("gdi", default=False, description="Enable GDI integration helpers on Windows")
        # CMake system dropped a number of source files
        # they're correctly added as of 11.5
        patch("harfbuzz_10_0_cmake_add_missing_table_sources.patch", when="@10:11.1")
        patch("harfbuzz_11_2_cmake_add_missing_table_sources.patch", when="@11.2:11.3")
        patch("harfbuzz_11_4_cmake_add_missing_table_sources.patch", when="@11.4")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    with when("build_system=meson"):
        depends_on("meson@0.60:", when="@11.1:")
        depends_on("meson@0.55:", when="@3.2.1:")
        depends_on("meson@0.52:")
        # harfbuzz's Meson only supports autotools based
        # freetype
        depends_on("freetype build_system=autotools")
        depends_on("cairo build_system=meson")

    for plat in ["linux", "darwin", "freebsd"]:
        with when(f"platform={plat}"):
            variant("gobject", default=False, description="Enable GObject introspection")
            variant(
                "utils",
                default=False,
                when="build_system=cmake",
                description="Build harfbuzz utils",
            )
            depends_on("pkgconfig", type="build")
            depends_on("glib")
            depends_on("gobject-introspection")
            depends_on("cairo+pdf+ft")

    depends_on("icu4c")
    depends_on("freetype")
    depends_on("zlib-api")
    depends_on("graphite2", when="+graphite2")

    conflicts("%intel", msg="harfbuzz-2.3.1 does not build with the Intel compiler")

    # Function borrowed from superlu
    def flag_handler(self, name, flags):
        flags = list(flags)
        if name == "cxxflags":
            flags.append(self.compiler.cxx11_flag)
        if name == "cflags":
            if self.spec.satisfies("%gcc@:5.1"):
                flags.append("-std=gnu99")
        return None, None, flags

    def setup_run_environment(self, env: EnvironmentModifications) -> None:
        env.prepend_path("GI_TYPELIB_PATH", join_path(self.prefix.lib, "girepository-1.0"))

    def setup_dependent_run_environment(
        self, env: EnvironmentModifications, dependent_spec: Spec
    ) -> None:
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)
        env.prepend_path("GI_TYPELIB_PATH", join_path(self.prefix.lib, "girepository-1.0"))

    @when("@:8")
    def patch(self):
        change_sed_delimiter("@", ";", "src/Makefile.in")


class SetupEnvironment:
    def setup_dependent_build_environment(
        self, env: EnvironmentModifications, dependent_spec: Spec
    ) -> None:
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)
        env.prepend_path("GI_TYPELIB_PATH", join_path(self.prefix.lib, "girepository-1.0"))


class MesonBuilder(meson.MesonBuilder, SetupEnvironment):
    def meson_args(self):
        graphite2 = "enabled" if self.pkg.spec.satisfies("+graphite2") else "disabled"
        coretext = "enabled" if self.pkg.spec.satisfies("+coretext") else "disabled"
        introspection = "enabled" if self.pkg.spec.satisfies("+gobject") else "disabled"
        config_args = [
            # disable building of gtk-doc files following #9885 and #9771
            "-Ddocs=disabled",
            "-Dfreetype=enabled",
            f"-Dgraphite2={graphite2}",
            f"-Dcoretext={coretext}",
            f"-Dintrospection={introspection}",
        ]
        if IS_WINDOWS:
            config_args.extend(["-Dcairo=disabled", "-Dglib=disabled"])
        return config_args


class AutotoolsBuilder(autotools.AutotoolsBuilder, SetupEnvironment):
    def configure_args(self):
        args = []

        # disable building of gtk-doc files following #9771
        args.append("--disable-gtk-doc-html")
        true = which("true")
        args.append(f"GTKDOC_CHECK={true}")
        args.append(f"GTKDOC_CHECK_PATH={true}")
        args.append(f"GTKDOC_MKPDF={true}")
        args.append(f"GTKDOC_REBASE={true}")
        args.extend(self.with_or_without("graphite2"))
        args.extend(self.with_or_without("coretext"))
        args.extend(self.with_or_without("gobject"))

        return args


class CMakeBuilder(cmake.CMakeBuilder, SetupEnvironment):
    def cmake_args(self):
        use_gobject = self.spec.satisfies("+gobject")
        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define("HB_HAVE_FREETYPE", True),
            self.define("HB_HAVE_ICU", True),
            self.define_from_variant("HB_HAVE_GRAPHITE2", "graphite2"),
            self.define_from_variant("HB_HAVE_UNISCRIBE", "uniscribe"),
            self.define_from_variant("HB_HAVE_GDI", "gdi"),
            self.define_from_variant("HB_HAVE_DIRECTWRITE", "directwrite"),
            self.define_from_variant("HB_HAVE_CORETEXT", "coretext"),
            self.define("HB_HAVE_GLIB", use_gobject),
            self.define("HB_HAVE_CAIRO", use_gobject),
            self.define("HB_BUILD_UTILS", use_gobject and self.spec.satisfies("+utils")),
            self.define("HB_HAVE_GOBJECT", use_gobject),
            self.define("HB_HAVE_INTROSPECTION", use_gobject),
        ]

        return args
