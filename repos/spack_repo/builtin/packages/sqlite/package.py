# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import re
import sys
from tempfile import NamedTemporaryFile

from spack_repo.builtin.build_systems import autotools, nmake
from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.nmake import NMakePackage

from spack.package import *

is_windows = sys.platform == "win32"


class Sqlite(AutotoolsPackage, NMakePackage):
    """SQLite is a C-language library that implements a small, fast,
    self-contained, high-reliability, full-featured, SQL database engine.
    """

    homepage = "https://www.sqlite.org"
    tags = ["windows"]


    # All versions prior to 3.26.0 are vulnerable to Magellan when FTS
    # is enabled, see https://blade.tencent.com/magellan/index_en.html

    # no hard readline dep on Windows + no variant support, makefile has minimal to no options
    for plat in ["linux", "darwin", "freebsd"]:
        variant(
            "column_metadata",
            default=True,
            description="Build with COLUMN_METADATA",
            when=f"platform={plat}",
        )
        variant(
            "dynamic_extensions",
            default=True,
            description="Support loadable extensions",
            when=f"@:3.48 platform={plat}",
        )

        depends_on("readline", when=f"platform={plat}")

    variant("fts", default=True, description="Include fts4 and fts5 support")

    # functions variant is always available on Windows platform, otherwise is tied
    # to +dynamic_extensions
    function_condition = "platform=windows" if is_windows else "+dynamic_extensions"
    variant(
        "functions",
        default=is_windows,
        description="Provide mathematical and string extension functions for SQL "
        "queries using the loadable extensions mechanism",
        when=f"{function_condition}",
    )
    variant("rtree", default=True, description="Build with Rtree module")

    depends_on("c", type="build")  # generated

    depends_on("zlib-api")
    depends_on("tcl", when="platform=windows")

    # See https://blade.tencent.com/magellan/index_en.html
    conflicts("+fts", when="@:3.25")

    resource(
        name="extension-functions",
        url="https://www.sqlite.org/contrib/download/extension-functions.c/download/extension-functions.c?get=25",
        sha256="991b40fe8b2799edc215f7260b890f14a833512c9d9896aa080891330ffe4052",
        expand=False,
        placement={"extension-functions.c?get=25": "extension-functions.c"},
        when="+functions",
    )

    # On some platforms (e.g., PPC) the include chain includes termios.h which
    # defines a macro B0. Sqlite has a shell.c source file that declares a
    # variable named B0 and will fail to compile when the macro is found. The
    # following patch undefines the macro in shell.c

    # Starting version 3.17.0, SQLite uses compiler built-ins
    # __builtin_sub_overflow(), __builtin_add_overflow(), and
    # __builtin_mul_overflow(), which are not supported by Intel compiler.
    # Starting version 3.21.0 SQLite doesn't use the built-ins if Intel
    # compiler is used.


    build_system("autotools", "nmake")

    executables = ["^sqlite3$"]

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        # `sqlite3 --version` prints only the version number, timestamp, commit
        # hash(?) but not the program name. As a basic sanity check, the code
        # calls re.match() and attempts to match the ISO 8601 date following the
        # version number as well.
        match = re.match(r"(\S+) \d{4}-\d{2}-\d{2}", output)
        return match.group(1) if match else None

    @classmethod
    def determine_variants(cls, exes, version_str):
        all_variants = []

        def call(exe, query):
            with NamedTemporaryFile(mode="w", buffering=1) as sqlite_stdin:
                sqlite_stdin.write(query + "\n")
                e = Executable(exe)
                e(
                    fail_on_error=False,
                    input=sqlite_stdin.name,
                    output=os.devnull,
                    error=os.devnull,
                )
            return e.returncode

        def get_variant(name, has_variant):
            fmt = "+{:s}" if has_variant else "~{:s}"
            return fmt.format(name)

        for exe in exes:
            variants = []

            # check for fts
            def query_fts(version):
                return "CREATE VIRTUAL TABLE name USING fts{:d}(sender, title, body);".format(
                    version
                )

            rc_fts4 = call(exe, query_fts(4))
            rc_fts5 = call(exe, query_fts(5))
            variants.append(get_variant("fts", rc_fts4 == 0 and rc_fts5 == 0))

            # check for functions
            # SQL query taken from extension-functions.c usage instructions
            query_functions = "SELECT load_extension('libsqlitefunctions');"
            rc_functions = call(exe, query_functions)
            variants.append(get_variant("functions", rc_functions == 0))

            # check for rtree
            query_rtree = "CREATE VIRTUAL TABLE name USING rtree(id, x, y);"
            rc_rtree = call(exe, query_rtree)
            variants.append(get_variant("rtree", rc_rtree == 0))

            # TODO: column_metadata, dynamic_extensions

            all_variants.append("".join(variants))

        return all_variants

    def url_for_version(self, version):
        if len(version) < 3:
            raise ValueError(f"Unsupported sqlite version: {version}")
        # See https://www.sqlite.org/chronology.html for version -> year
        # correspondence.
        if version >= Version("3.51.2"):
            year = "2026"
        elif version >= Version("3.48.0"):
            year = "2025"
        elif version >= Version("3.45.0"):
            year = "2024"
        elif version >= Version("3.41.0"):
            year = "2023"
        elif version >= Version("3.37.2"):
            year = "2022"
        elif version >= Version("3.34.1"):
            year = "2021"
        elif version >= Version("3.31.0"):
            year = "2020"
        elif version >= Version("3.27.0"):
            year = "2019"
        elif version >= Version("3.22.0"):
            year = "2018"
        elif version >= Version("3.16.0"):
            year = "2017"
        elif version >= Version("3.10.0"):
            year = "2016"
        elif version >= Version("3.8.8"):
            year = "2015"
        elif version >= Version("3.8.3"):
            year = "2014"
        elif version >= Version("3.7.16"):
            year = "2013"
        else:
            raise ValueError(f"Unsupported sqlite version {version}")
        return f"https://www.sqlite.org/{year}/sqlite-autoconf-{version[0]}{version[1]:02}{version[2]:02}00.tar.gz"

    @property
    def libs(self):
        prefix = "lib" if sys.platform != "win32" else ""
        return find_libraries(f"{prefix}sqlite3", root=self.prefix.lib, runtime=False)

    def test_example(self):
        """check example table dump"""

        test_data_dir = self.test_suite.current_test_data_dir
        db_filename = test_data_dir.join("packages.db")

        # Ensure the database only contains one table
        sqlite3 = which(self.prefix.bin.sqlite3)
        out = sqlite3(db_filename, ".tables", output=str.split, error=str.split)
        assert "packages" in out

        # Ensure the database dump matches expectations, where special
        # characters are replaced with spaces in the expected and actual
        # output to avoid pattern errors.
        expected = get_escaped_text_output(test_data_dir.join("dump.out"))
        out = sqlite3(db_filename, ".dump", output=str.split, error=str.split)
        check_outputs(expected, out)

    def test_version(self):
        """ensure version is expected"""
        vers_str = str(self.spec.version)

        sqlite3 = which(self.prefix.bin.sqlite3, required=True)
        out = sqlite3("-version", output=str.split, error=str.split)
        assert vers_str in out


class AutotoolsBuilder(autotools.AutotoolsBuilder):
    def configure_args(self):
        args = []

        args.extend(self.enable_or_disable("fts4", variant="fts"))
        args.extend(self.enable_or_disable("fts5", variant="fts"))

        # Ref: https://www.sqlite.org/rtree.html
        args.extend(self.enable_or_disable("rtree"))

        # Ref: https://www.sqlite.org/loadext.html
        args.extend(self.enable_or_disable("dynamic-extensions", variant="dynamic_extensions"))

        # Ref: https://www.sqlite.org/compile.html
        if "+column_metadata" in self.spec:
            args.append("CPPFLAGS=-DSQLITE_ENABLE_COLUMN_METADATA=1")

        return args

    @run_after("install")
    def build_libsqlitefunctions(self):
        if "+functions" in self.spec:
            libraryname = "libsqlitefunctions." + dso_suffix
            cc = Executable(spack_cc)
            cc(
                self.pkg.compiler.cc_pic_flag,
                "-lm",
                "-shared",
                "extension-functions.c",
                "-o",
                libraryname,
            )
            install(libraryname, self.prefix.lib)


class NMakeBuilder(nmake.NMakeBuilder):
    @property
    def makefile_name(self):
        return "Makefile.msc"

    def nmake_args(self):
        enable_fts = "1" if "+fts" in self.spec else "0"
        enable_rtree = "1" if "+rtree" in self.spec else "0"
        enable_functions = "1" if "+functions" in self.spec else "0"

        opts = (
            "OPTS="
            f"-DSQLITE_ENABLE_FTS3={enable_fts} "
            f"-DSQLITE_ENABLE_FTS4={enable_fts} "
            f"-DSQLITE_ENABLE_FTS5={enable_fts} "
            f"-DSQLITE_ENABLE_RTREE={enable_rtree} "
            "-DSQLITE_ENABLE_JSON1=1 "
            "-DSQLITE_ENABLE_GEOPOLY=1 "
            "-DSQLITE_ENABLE_SESSION=1 "
            "-DSQLITE_ENABLE_PREUPDATE_HOOK=1 "
            "-DSQLITE_ENABLE_SERIALIZE=1 "
            f"-DSQLITE_ENABLE_MATH_FUNCTIONS={enable_functions}"
        )

        return ["USE_NATIVE_LIBPATHS=1", "DYNAMIC_SHELL=1", opts]

    def install(self, pkg, spec, prefix):
        with working_dir(self.build_directory):
            mkdirp(prefix.include)
            mkdirp(prefix.lib)
            mkdirp(prefix.bin)
            install(f"{self.build_directory}\\*.exe", prefix.bin)
            install(f"{self.build_directory}\\*.dll", prefix.bin)
            install(f"{self.build_directory}\\*.lib", prefix.lib)
            install(f"{self.build_directory}\\*.h", prefix.include)
