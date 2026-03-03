# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import glob
import os
import sys

from spack_repo.builtin.build_systems import compiler
from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.compiler import CompilerPackage
from spack_repo.builtin.build_systems.gnu import GNUMirrorPackage

from spack.package import *


class Gcc(AutotoolsPackage, GNUMirrorPackage, CompilerPackage):
    """The GNU Compiler Collection includes front ends for C, C++, Objective-C,
    Fortran, Ada, and Go, as well as libraries for these languages."""

    homepage = "https://gcc.gnu.org"
    gnu_mirror_path = "gcc/gcc-9.2.0/gcc-9.2.0.tar.xz"
    git = "git://gcc.gnu.org/git/gcc.git"
    list_url = "https://ftp.gnu.org/gnu/gcc/"
    list_depth = 1
    keep_werror = "all"


    provides("c", "cxx", when="languages=c,c++")
    provides("c", when="languages=c")
    provides("cxx", when="languages=c++")
    provides("fortran", when="languages=fortran")

    version("master", branch="master")

    # Latest stable
    version("15.2.0", sha256="438fd996826b0c82485a29da03a72d71d6e3541a83ec702df4271f6fe025d24e")

    # Previous stable series releases
    version("15.1.0", sha256="e2b09ec21660f01fecffb715e0120265216943f038d0e48a9868713e54f06cea")

    # Final releases of previous versions
    version("11.5.0", sha256="a6e21868ead545cf87f0c01f84276e4b5281d672098591c1c896241f09363478")

    # Used in the tutorial

    # Deprecated older non-final releases
    with default_args(deprecated=True):










        version("4.9.2", sha256="2020c98295856aa13fda0f2f3a4794490757fc24bcca918d52cc8b4917b972dd")
        version("4.9.1", sha256="d334781a124ada6f38e63b545e2a3b8c2183049515a1abab6d513f109f1d717e")
        version("4.8.4", sha256="4a80aa23798b8e9b5793494b8c976b39b8d9aa2e53cd5ed5534aff662a7f8695")

    # We specifically do not add 'all' variant here because:
    # (i) Ada, D, Go, Jit, and Objective-C++ are not default languages.
    # In that respect, the name 'all' is rather misleading.
    # (ii) Languages other than c,c++,fortran are prone to configure bug in GCC
    # For example, 'java' appears to ignore custom location of zlib
    # (iii) meaning of 'all' changes with GCC version, i.e. 'java' is not part
    # of gcc7. Correctly specifying conflicts() and depends_on() in such a
    # case is a PITA.
    #
    # Also note that some languages get enabled by the configure scripts even if not listed in the
    # arguments. For example, c++ is enabled when the bootstrapping is enabled and lto is enabled
    # when the link time optimization support is enabled.
    variant(
        "languages",
        default="c,c++,fortran",
        values=(
            "ada",
            "brig",
            "c",
            "c++",
            "d",
            "fortran",
            "go",
            "java",
            "jit",
            "lto",
            "objc",
            "obj-c++",
        ),
        multi=True,
        description="Compilers and runtime libraries to build",
    )
    variant("binutils", default=True, description="Use binutils linker and assembler")
    variant("mold", default=False, description="Use mold as the linker by default", when="@12:")
    variant(
        "piclibs", default=False, description="Build PIC versions of libgfortran.a and libstdc++.a"
    )
    variant("strip", default=False, description="Strip executables to reduce installation size")
    variant("nvptx", default=False, description="Target nvptx offloading to NVIDIA GPUs")
    variant("bootstrap", default=True, description="Enable 3-stage bootstrap")
    variant(
        "graphite", default=False, description="Enable Graphite loop optimizations (requires ISL)"
    )
    variant(
        "build_type",
        default="RelWithDebInfo",
        values=("Debug", "Release", "RelWithDebInfo", "MinSizeRel"),
        description="CMake-like build type. "
        "Debug: -O0 -g; Release: -O3; "
        "RelWithDebInfo: -O2 -g; MinSizeRel: -Os",
    )
    variant(
        "profiled", default=False, description="Use Profile Guided Optimization", when="+bootstrap"
    )



    # https://gcc.gnu.org/install/prerequisites.html
    # mawk is not sufficient for go support
    # dependencies required for git versions


    # GCC 7.3 does not compile with newer releases on some platforms, see
    #   https://github.com/spack/spack/issues/6902#issuecomment-433030376
    # Already released GCC versions do not support any newer version of ISL
    #   GCC 5.4 https://github.com/spack/spack/issues/6902#issuecomment-433072097
    #   GCC 7.3 https://github.com/spack/spack/issues/6902#issuecomment-433030376
    #   GCC 9+  https://gcc.gnu.org/bugzilla/show_bug.cgi?id=86724
    with when("+graphite"):
        depends_on("isl@0.14", when="@5.0:5.2")
        depends_on("isl@0.15", when="@5.3:5.9")
        depends_on("isl@0.15:0.18", when="@6:8.9")
        depends_on("isl@0.15:0.20", when="@9:9.9")
        depends_on("isl@0.15:", when="@10:")

    depends_on("zlib-api", when="@6:")
    depends_on("zstd", when="@10:")
    depends_on("diffutils", type="build")

    # The server is sometimes a bit slow to respond
    timeout = {"timeout": 60}

    # TODO: integrate these libraries.
    # depends_on('ppl')
    # depends_on('cloog')

    # https://gcc.gnu.org/install/test.html

    # See https://go.dev/doc/install/gccgo#Releases
    with when("languages=go"):
        provides("go-or-gccgo-bootstrap@:1.0", when="@4.7.1:")
    # For a list of valid languages for a specific release,

    # BRIG does not seem to be supported on macOS

    # GCC 4.8 added a 'c' language. I'm sure C was always built,
    # but this is the first version that accepts 'c' as a valid language.

    # The GCC Java frontend and associated libjava runtime library
    # have been removed from GCC as of GCC 7.
    # See https://gcc.gnu.org/gcc-7/changes.html

    # GCC 5 added the ability to build GCC as a Just-In-Time compiler.
    # See https://gcc.gnu.org/gcc-5/changes.html

    with when("languages=d"):
        # Support for the D programming language has been added to GCC 9.
        # See https://gcc.gnu.org/gcc-9/changes.html#d
        conflicts("@:8", msg="support for D has been added in GCC 9.1")

        # Versions of GDC prior to 12 can be built with an ISO C++11 compiler. Starting version 12,
        # the D frontend requires a working GDC. Moreover, it is strongly recommended to use an
        # older version of GDC to build GDC.
        # See https://gcc.gnu.org/install/prerequisites.html#GDC-prerequisite
        with when("@12:"):
            # All versions starting 12 have to be built GCC:
            requires("%gcc")

            # And it has to be GCC older than the version we build:
            vv = ["11", "12.1.0", "12.2.0"]
            for prev_v, curr_v in zip(vv, vv[1:]):
                conflicts(
                    "%gcc@{0}:".format(curr_v),
                    when="@{0}".format(curr_v),
                    msg="'gcc@{0} languages=d' requires '%gcc@:{1}' "
                    "with the D language support".format(curr_v, prev_v),
                )

            # See https://github.com/D-Programming-GDC/gdc
            # We, however, require at least the oldest version that officially supports GDC. It is
            # also a good opportunity to tell the users that they need a working GDC:

    # GPU offload backend supported by limited languages
    with when("+nvptx"):
        conflicts("languages=d")

    # Newlib version table
    newlib_shasum = {
        "3.0.0.20180831": "3ad3664f227357df15ff34e954bfd9f501009a647667cd307bf0658aefd6eb5b",
        "3.3.0": "58dd9e3eaedf519360d92d84205c3deef0b3fc286685d1c562e245914ef72c66",
        "4.1.0": "f296e372f51324224d387cc116dc37a6bd397198756746f93a2b02e9a5d40154",
        "4.2.0.20211231": "c3a0e8b63bc3bef1aeee4ca3906b53b3b86c8d139867607369cb2915ffc54435",
        "4.3.0.20230120": "83a62a99af59e38eb9b0c58ed092ee24d700fff43a22c03e433955113ef35150",
        "4.4.0.20231231": "0c166a39e1bf0951dfafcd68949fe0e4b6d3658081d6282f39aeefc6310f2f13",
        "4.5.0.20241231": "33f12605e0054965996c25c1382b3e463b0af91799001f5bb8c0630f2ec8c852",
    }

    with when("+nvptx"):
        nvptx_newlib_ver = "4.5.0.20241231"
        resource(
            name="newlib",
            url="ftp://sourceware.org/pub/newlib/newlib-{0}.tar.gz".format(nvptx_newlib_ver),
            sha256=newlib_shasum[nvptx_newlib_ver],
            destination="newlibsource",
            fetch_options=timeout,
        )

        nvptx_tools_ver = "2023-09-13"

        # NVPTX offloading supported in 7 and later by limited languages
        conflicts("@:6", msg="NVPTX only supported in gcc 7 and above")

        # NVPTX build disables bootstrap
        conflicts("+bootstrap")

    # Binutils can't build ld on macOS

    # Bootstrap comparison failure:
    #   see https://github.com/spack/spack/issues/23296
    #   https://gcc.gnu.org/bugzilla/show_bug.cgi?id=100340
    #   on XCode 12.5

    requires(
        "@11.3:",
        when="target=aarch64: platform=darwin",
        msg="Only GCC 11.3+ support aarch64-darwin",
    )

    # GCC 11 requires GCC 4.8 or later (https://gcc.gnu.org/gcc-11/changes.html)

    # https://github.com/iains/gcc-12-branch/issues/6

    # Applies
    # https://github.com/gcc-mirror/gcc/commit/ea2798892de373b14f9fc7ae8a0d820eaddca98c,
    # which fixes an incorrectly applied fixincludes rule for pthread.h, making
    # the installed GCC not portable across different glibc versions. Original
    # GCC bug report: https://gcc.gnu.org/bugzilla/show_bug.cgi?id=118009. For
    # GCC 15 we can directly use the upstream patch. For GCC 12-14 the patch
    # has been backported. The patch is not applied to GCC 11 since the "fixinclude"
    # is in fact needed for that version (see GCC commit description). Older versions
    # have not been checked or tested.
    patch(
        "https://github.com/gcc-mirror/gcc/commit/ea2798892de373b14f9fc7ae8a0d820eaddca98c.patch?full_index=1",
        sha256="0999dbf856725566373f25a6f192a3520ea036db8e1f31928aae9750e6e38be7",
        when="@15:15.2",
    )
    patch("fixincludes-gcc-13-14.patch", when="@13:14")
    patch("fixincludes-gcc-12.4.patch", when="@12.4:12")
    patch("fixincludes-gcc-12.1.patch", when="@12:12.3")

    if sys.platform == "darwin":
        # Fix parallel build on APFS filesystem
        # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=81797
        if macos_version() >= Version("10.13"):
            patch("darwin/apfs.patch", when="@5.5.0,6.1:6.4,7.1:7.3")
            # from homebrew via macports
            # https://trac.macports.org/ticket/56502#no1
            # see also: https://gcc.gnu.org/bugzilla/show_bug.cgi?id=83531
            patch("darwin/headers-10.13-fix.patch", when="@5.5.0")
        if macos_version() >= Version("10.14"):
            # Fix system headers for Mojave SDK:
            # https://github.com/Homebrew/homebrew-core/pull/39041
            patch(
                "https://raw.githubusercontent.com/Homebrew/formula-patches/b8b8e65e/gcc/8.3.0-xcode-bug-_Atomic-fix.patch",
                sha256="33ee92bf678586357ee8ab9d2faddf807e671ad37b97afdd102d5d153d03ca84",
                when="@6:8.3",
            )

            # See https://raw.githubusercontent.com/Homebrew/homebrew-core/3b7db4457ac64a31e3bbffc54b04c4bd824a4a4a/Formula/gcc.rb
            patch(
                "https://github.com/iains/gcc-darwin-arm64/commit/20f61faaed3b335d792e38892d826054d2ac9f15.patch?full_index=1",
                sha256="c0605179a856ca046d093c13cea4d2e024809ec2ad4bf3708543fc3d2e60504b",
            )

        # aarch64-darwin support from Iain Sandoe's branch
        patch(
            "https://github.com/iains/gcc-14-branch/compare/04696df09633baf97cdbbdd6e9929b9d472161d3..a495b2dded281beeafec91074e4e82a5a3df8104.patch?full_index=1",
            sha256="838cf070bec5468340018bf003f714f6340c562b878f3244303d2b7ba9949ccd",
            when="@14.1.0 target=aarch64:",
        )

        patch(
            "https://github.com/iains/gcc-13-branch/compare/c891d8dc23e1a46ad9f3e757d09e57b500d40044..gcc-13.2-darwin-r0.patch?full_index=1",
            sha256="36d2c04d487edb6792b48dedae6936f8b864b6f969bd3fd03763e072d471c022",
            when="@13.1.0 target=aarch64:",
        )
        # 14.2.0 cannot bootstrap on x86_64
    # Older versions do not compile with newer versions of glibc
    # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=81712
    # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=81066
    # https://bugs.busybox.net/show_bug.cgi?id=10061
    # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=85835

    # this patch removes cylades support from gcc-5 and allows gcc-5 to be built
    # with newer glibc versions.

    # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=95005

    # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=100102

    # libstdc++: Fix inconsistent noexcept-specific for valarray begin/end

    # patch ICE on aarch64 in tree-vect-slp, cf: https://gcc.gnu.org/bugzilla/show_bug.cgi?id=111478
    # patch taken from releases/gcc-12 branch
    # patch taken from releases/gcc-13 branch

    # see https://gcc.gnu.org/gcc-11/changes.html 11.5 Caveats

    build_directory = "spack-build"

    compiler_languages = ["c", "cxx", "fortran", "d", "go"]

    c_names = ["gcc"]
    cxx_names = ["g++"]
    fortran_names = ["gfortran"]
    d_names = ["gdc"]
    go_names = ["gccgo"]
    compiler_suffixes = [r"-mp-\d+(?:\.\d+)?", r"-\d+(?:\.\d+)?", r"\d\d"]
    compiler_version_regex = r"([0-9.]+)"
    compiler_version_argument = ("-dumpfullversion", "-dumpversion")

    compiler_wrapper_link_paths = {
        "c": os.path.join("gcc", "gcc"),
        "cxx": os.path.join("gcc", "g++"),
        "fortran": os.path.join("gcc", "gfortran"),
    }

    debug_flags = ["-g", "-gstabs+", "-gstabs", "-gxcoff+", "-gxcoff", "-gvms"]
    opt_flags = ["-O", "-O0", "-O1", "-O2", "-O3", "-Os", "-Ofast", "-Og"]

    implicit_rpath_libs = ["libgcc", "libgfortran"]
    stdcxx_libs = ("-lstdc++",)

    # https://gcc.gnu.org/install/configure.html
    # Common code for nvptx and amdgcn to link newlib source directory
    newlib_linked = False

    # Copy nvptx-tools into the GCC install prefix
    def copy_nvptx_tools(self):
        nvptx_tools_bin_path = self.spec["nvptx-tools"].prefix.bin
        gcc_bin_path = self.prefix.bin
        mkdirp(gcc_bin_path)
        copy_list = ["as", "ld", "nm", "run", "run-single"]
        for file in copy_list:
            fullname = f"nvptx-none-{file}"
            copy(join_path(nvptx_tools_bin_path, fullname), join_path(gcc_bin_path, fullname))
        link_list = ["ar", "ranlib"]
        for file in link_list:
            fullname = f"nvptx-none-{file}"
            orig_target = readlink(join_path(nvptx_tools_bin_path, fullname))
            symlink(orig_target, join_path(gcc_bin_path, fullname))
        util_dir_path = join_path(self.prefix, "nvptx-none", "bin")
        mkdirp(util_dir_path)
        util_list = ["ar", "as", "ld", "nm", "ranlib"]
        for file in util_list:
            rel_target = join_path("..", "..", "bin", f"nvptx-none-{file}")
            dest_link = join_path(util_dir_path, file)
            symlink(rel_target, dest_link)

    # run configure/make/make(install) for the nvptx-none target
    # before running the host compiler phases
    @run_before("configure")
    def nvptx_install(self):
        spec = self.spec
        prefix = self.prefix

        if not spec.satisfies("+nvptx"):
            return

        # config.guess returns the host triple, e.g. "x86_64-pc-linux-gnu"
        guess = Executable("./config.guess")
        targetguess = guess(output=str).rstrip("\n")

        options = getattr(self, "configure_flag_args", [])
        options += ["--prefix={0}".format(prefix)]

        options += [
            "--with-cuda-driver-include={0}".format(spec["cuda"].prefix.include),
            "--with-cuda-driver-lib={0}".format(spec["cuda"].libs.directories[0]),
        ]

        self.copy_nvptx_tools()

        self.link_newlib()

        # self.build_directory = 'spack-build-nvptx'
        with working_dir("spack-build-nvptx", create=True):
            options = [
                "--prefix={0}".format(prefix),
                "--enable-languages={0}".format(",".join(spec.variants["languages"].value)),
                "--with-mpfr={0}".format(spec["mpfr"].prefix),
                "--with-gmp={0}".format(spec["gmp"].prefix),
                "--target=nvptx-none",
                "--with-build-time-tools={0}".format(join_path(prefix, "nvptx-none", "bin")),
                "--enable-as-accelerator-for={0}".format(targetguess),
                "--disable-sjlj-exceptions",
                "--enable-newlib-io-long-long",
            ]

            configure = Executable("../configure")
            configure(*options)
            make()
            make("install")

    @property
    def build_targets(self):
        if self.spec.satisfies("+profiled"):
            return ["profiledbootstrap"]
        return []

    @property
    def install_targets(self):
        if self.spec.satisfies("+strip"):
            return ["install-strip"]
        return ["install"]

    @property
    def spec_dir(self):
        # e.g. lib/gcc/x86_64-unknown-linux-gnu/4.9.2
        spec_dir = glob.glob(f"{self.prefix.lib}/gcc/*/*")
        return spec_dir[0] if spec_dir else None

    @run_after("install")
    def write_specs_file(self):
        """(1) inject an rpath to its runtime library dir, (2) add a default programs search path
        to <binutils>/bin."""
        if not self.spec_dir:
            tty.warn(f"Could not install specs for {self.spec.format('{name}{@version}')}.")
            return

        # Find which directories have shared libraries
        for dir in ["lib64", "lib"]:
            libdir = join_path(self.prefix, dir)
            if glob.glob(join_path(libdir, "libgcc_s.*")):
                rpath_dir = libdir
                break
        else:
            tty.warn("No dynamic libraries found in lib/lib64")
            rpath_dir = None

        specs_file = join_path(self.spec_dir, "specs")
        with open(specs_file, "w") as f:
            # can't extend the builtins without dumping them first
            f.write(self.command("-dumpspecs", output=str, error=os.devnull).strip())

            f.write("\n\n# Generated by Spack\n\n")

            # rpath
            if rpath_dir:
                f.write(f"*link_libgcc:\n+ -rpath {rpath_dir}\n\n")

            # programs search path
            if self.spec.satisfies("+binutils"):
                f.write(f"*self_spec:\n+ -B{self.spec['binutils'].prefix.bin}\n\n")

            # set -fuse-ld=mold as the default linker when +mold
            if self.spec.satisfies("+mold"):
                f.write(
                    f"*self_spec:\n+ -B{self.spec['mold'].prefix.bin} "
                    "%{!fuse-ld*:-fuse-ld=mold}\n\n"
                )

        set_install_permissions(specs_file)
        tty.info(f"Wrote new spec file to {specs_file}")

        # Do the same thing for libgomp on offload-enabled builds
        if self.spec.satisfies("+nvptx"):
            for dir in ["lib64", "lib"]:
                libdir = join_path(self.prefix, dir)
                if glob.glob(join_path(libdir, "libgomp.*")):
                    libgomp_dir = libdir
                    break
            else:
                tty.warn("libgomp dynamic library not found in lib/lib64")
                libgomp_dir = None

            if libgomp_dir:
                libgomp_spec_file = join_path(libgomp_dir, "libgomp.spec")
                copy(libgomp_spec_file, libgomp_spec_file + ".orig")
                with open(libgomp_spec_file, "r+") as f:
                    lines = f.readlines()
                    f.seek(0)
                    for line in lines:
                        if line.startswith("*link_gomp:"):
                            f.write("\n\n# Generated by Spack\n\n")
                            f.write(line.strip("\n") + f" -rpath {libgomp_dir}\n\n")
                        else:
                            f.write(line)
                set_install_permissions(libgomp_spec_file)
                tty.info(f"Wrote new libgomp spec file to {libgomp_spec_file}")

    # The configure --sysroot doesn't propagate down into the sub-builds, e.g., libiberty.
    # Starting with SDK 26 and clang 17, limits.h amongst other sys includes aren't included
    # via other means, resulting in a failed build. Keep this for other builds for safety.
    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        if self.spec.satisfies("platform=darwin"):
            macos_sdk_path = Executable("xcrun")("--show-sdk-path", output=str).strip()
            env.set("CFLAGS", f"--sysroot {macos_sdk_path}")

    def setup_run_environment(self, env: EnvironmentModifications) -> None:
        if self.cc and self.spec.satisfies("languages=c"):
            env.set("CC", self.cc)

        if self.cxx and self.spec.satisfies("languages=c++"):
            env.set("CXX", self.cxx)

        if self.fortran and self.spec.satisfies("languages=fortran"):
            env.set("FC", self.fortran)
            env.set("F77", self.fortran)

    def detect_gdc(self):
        """Detect and return the path to GDC that belongs to the same instance of GCC that is used
        by self.compiler.

        If the path cannot be detected, raise InstallError with recommendations for the users on
        how to circumvent the problem.

        Should be use only if self.spec.satisfies("@12: languages=d")
        """
        # Detect GCC package in the directory of the GCC compiler
        # or in the $PATH if self.compiler.cc is not an absolute path:
        from spack.detection import by_path  # TODO: remove use of private Spack API

        compiler_dir = os.path.dirname(self.compiler.cc)
        detected_packages = by_path(
            [self.name], path_hints=([compiler_dir] if os.path.isdir(compiler_dir) else None)
        )

        # We consider only packages that satisfy the following constraint:
        required_spec = Spec("languages=c,c++,d")
        candidate_specs = [
            p.spec
            for p in filter(
                lambda p: p.spec.satisfies(required_spec), detected_packages.get(self.name, ())
            )
        ]

        if candidate_specs:
            # We now need to filter specs that match the compiler version:
            compiler_spec = Spec(repr(self.compiler.spec))

            # First, try to filter specs that satisfy the compiler spec:
            new_candidate_specs = list(
                filter(lambda s: s.satisfies(compiler_spec), candidate_specs)
            )

            # The compiler version might be more specific than what we can detect. For example, the
            # user might have "gcc@10.2.1-sys" as the compiler spec in compilers.yaml. In that
            # case, we end up with an empty list of candidates. To circumvent the problem, we try
            # to filter specs that are satisfied by the compiler spec:
            if not new_candidate_specs:
                new_candidate_specs = list(
                    filter(lambda s: compiler_spec.satisfies(s), candidate_specs)
                )

            candidate_specs = new_candidate_specs

        error_nl = "\n    "  # see SpackError.__str__()

        if not candidate_specs:
            raise InstallError(
                "Cannot detect GDC",
                long_msg="Starting version 12, the D frontend requires a working GDC."
                "{0}You can install it with Spack by running:"
                "{0}{0}spack install gcc@9:11 languages=c,c++,d"
                "{0}{0}Once that has finished, you will need to add it to your compilers.yaml file"
                "{0}and use it to install this spec (i.e. {1} ...).".format(
                    error_nl, self.spec.format("{name}{@version} {variants.languages}")
                ),
            )
        elif len(candidate_specs) == 0:
            return candidate_specs[0].extra_attributes["compilers"]["d"]
        else:
            # It is rather unlikely to end up here but let us try to resolve the ambiguity:
            candidate_gdc = candidate_specs[0].extra_attributes["compilers"]["d"]
            if all(
                candidate_gdc == s.extra_attributes["compilers"]["d"] for s in candidate_specs[1:]
            ):
                # It does not matter which one we take if they are all the same:
                return candidate_gdc
            else:
                raise InstallError(
                    "Cannot resolve ambiguity when detecting GDC that belongs to %{0}".format(
                        self.compiler.spec
                    ),
                    long_msg="The candidates are:{0}{0}{1}{0}".format(
                        error_nl,
                        error_nl.join(
                            "{0} (cc: {1})".format(
                                s.extra_attributes["compilers"]["d"],
                                s.extra_attributes["compilers"]["c"],
                            )
                            for s in candidate_specs
                        ),
                    ),
                )

    @classmethod
    def runtime_constraints(cls, *, spec, pkg):
        """Callback function to inject runtime-related rules into the solver.

        Rule-injection is obtained through method calls of the ``pkg`` argument.

        Documentation for this function is temporary. When the API will be in its final state,
        we'll document the behavior at https://spack.readthedocs.io/en/latest/

        Args:
            spec: spec that will inject runtime dependencies
            pkg: object used to forward information to the solver
        """
        for language in ("c", "cxx", "fortran"):
            pkg("*").depends_on(
                f"gcc-runtime@{spec.version}:",
                when=f"%[deptypes=build virtuals={language}] {spec.name}@{spec.versions}",
                type="link",
                description=f"Inject gcc-runtime when gcc is used as a {language} compiler",
            )

        gfortran_str = "libgfortran@5"
        if spec.satisfies("gcc@:6"):
            gfortran_str = "libgfortran@3"
        elif spec.satisfies("gcc@7"):
            gfortran_str = "libgfortran@4"

        for fortran_virtual in ("fortran-rt", gfortran_str):
            pkg("*").depends_on(
                fortran_virtual,
                when=f"%[deptypes=build virtuals=fortran] {spec.name}@{spec.versions}",
                type="link",
                description=f"Add a dependency on '{gfortran_str}' for nodes compiled with "
                f"{spec} and using the 'fortran' language",
            )
        # The version of gcc-runtime is the same as the %gcc used to "compile" it
        pkg("gcc-runtime").requires(
            f"@{spec.versions}", when=f"%[deptypes=build] {spec.name}@{spec.versions}"
        )

        # If a node used %gcc@X.Y its dependencies must use gcc-runtime@:X.Y
        # (technically @:X is broader than ... <= @=X but this should work in practice)
        pkg("*").propagate(
            f"gcc@:{spec.version}", when=f"%[deptypes=build] {spec.name}@{spec.versions}"
        )

    def _post_buildcache_install_hook(self):
        if not self.spec.satisfies("platform=linux"):
            return

        # Setting up the runtime environment shouldn't be necessary here.
        relocation_args = []
        gcc = self.command
        specs_file = os.path.join(self.spec_dir, "specs")
        dryrun = gcc("test.c", "-###", output=os.devnull, error=str).strip()
        if not dryrun:
            tty.warn(f"Cannot relocate {specs_file}, compiler might not be working properly")
            return
        dynamic_linker = parse_dynamic_linker(dryrun)
        if not dynamic_linker:
            tty.warn(f"Cannot relocate {specs_file}, compiler might not be working properly")
            return

        libc = libc_from_dynamic_linker(dynamic_linker)
        if not libc:
            tty.warn(f"Cannot relocate {specs_file}, compiler might not be working properly")
            return

        # We search for crt1.o ourselves because `gcc -print-prile-name=crt1.o` can give a rather
        # convoluted relative path from a different prefix.
        startfile_prefix = _startfile_prefix(libc.external_path, dynamic_linker)
        if not startfile_prefix:
            tty.warn(f"Cannot relocate {specs_file}, compiler might not be working properly")
            return

        gcc_can_locate = lambda p: os.path.isabs(
            gcc(f"-print-file-name={p}", output=str, error=os.devnull).strip()
        )

        if not gcc_can_locate("crt1.o"):
            relocation_args.append(f"-B{startfile_prefix}")

        # libc headers may also be in a multiarch subdir.
        header_dir = _libc_include_dir_from_startfile_prefix(libc.external_path, startfile_prefix)
        if libc.name == "glibc":
            # glibc representative header
            header = "ieee754.h"
        else:
            # musl representative header
            header = "iso646.h"

        if header_dir and os.path.exists(os.path.join(header_dir, header)):
            relocation_args.append(f"-idirafter {header_dir}")
        else:
            tty.warn(
                f"Cannot relocate {specs_file} include directories, "
                f"compiler might not be working properly"
            )

        # Delete current spec files.
        try:
            os.unlink(specs_file)
        except OSError:
            pass

        # Write a new one and append flags for libc
        self.write_specs_file()

        if relocation_args:
            with open(specs_file, "a") as f:
                f.write(f"*self_spec:\n+ {' '.join(relocation_args)}\n\n")


def _libc_include_dir_from_startfile_prefix(
    libc_prefix: str, startfile_prefix: str
) -> Optional[str]:
    """Heuristic to determine the glibc include directory from the startfile prefix. Replaces
    $libc_prefix/lib*/<multiarch> with $libc_prefix/include/<multiarch>. This function does not
    check if the include directory actually exists or is correct."""
    parts = os.path.relpath(startfile_prefix, libc_prefix).split(os.path.sep)
    if parts[0] not in ("lib", "lib64", "libx32", "lib32"):
        return None
    parts[0] = "include"
    return os.path.join(libc_prefix, *parts)


def _startfile_prefix(prefix: str, compatible_with: str = sys.executable) -> Optional[str]:
    # Search for crt1.o at max depth 2 compatible with the ELF file provided in compatible_with.
    # This is useful for finding external libc startfiles on a multiarch system.
    try:
        compat = get_elf_compat(compatible_with)
        accept = lambda path: get_elf_compat(path) == compat
    except Exception:
        accept = lambda path: True

    stack = [(0, prefix)]
    while stack:
        depth, path = stack.pop()
        try:
            iterator = os.scandir(path)
        except OSError:
            continue
        with iterator:
            for entry in iterator:
                try:
                    if entry.is_dir(follow_symlinks=True):
                        if depth < 2:
                            stack.append((depth + 1, entry.path))
                    elif entry.name == "crt1.o" and accept(entry.path):
                        return path
                except Exception:
                    continue
    return None
