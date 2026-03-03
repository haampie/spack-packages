# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import re
import sys

from spack_repo.builtin.build_systems.cmake import CMakePackage, generator
from spack_repo.builtin.build_systems.compiler import CompilerPackage
from spack_repo.builtin.build_systems.cuda import CudaPackage

from spack.package import *


class LlvmDetection(PackageBase):
    """Base class to detect LLVM based compilers"""

    compiler_version_argument = "--version"
    c_names = ["clang"]
    cxx_names = ["clang++"]

    @classmethod
    def filter_detected_exes(cls, prefix, exes_in_prefix):
        # Executables like lldb-vscode-X are daemon listening on some port and would hang Spack
        # during detection. clang-cl, clang-cpp, etc. are dev tools that we don't need to test
        reject = re.compile(
            r"-(vscode|cpp|cl|ocl|gpu|tidy|rename|scan-deps|format|refactor|offload|"
            r"check|query|doc|move|extdef|apply|reorder|change-namespace|"
            r"include-fixer|import-test|dap|server|PerfectShuffle)"
        )
        return [x for x in exes_in_prefix if not reject.search(x)]


class Llvm(CMakePackage, CudaPackage, LlvmDetection, CompilerPackage):
    """The LLVM Project is a collection of modular and reusable compiler and
    toolchain technologies. Despite its name, LLVM has little to do
    with traditional virtual machines, though it does provide helpful
    libraries that can be used to build them. The name "LLVM" itself
    is not an acronym; it is the full name of the project.
    """

    homepage = "https://llvm.org/"
    url = "https://github.com/llvm/llvm-project/archive/llvmorg-7.1.0.tar.gz"
    list_url = "https://releases.llvm.org/download.html"
    git = "https://github.com/llvm/llvm-project"

    tags = ["e4s", "compiler"]

    generator("ninja")


    with default_args(deprecated=True):
        version(
            "19.1.2", sha256="622cb6c5e95a3bb7e9876c4696a65671f235bd836cfd0c096b272f6c2ada41e7"
        )

    # Final releases of previous versions

    variant(
        "clang", default=True, description="Build the LLVM C/C++/Objective-C compiler frontend"
    )
    variant("lldb", default=True, description="Build the LLVM debugger")

    variant("lld", default=True, description="Build the LLVM linker")
    variant("mlir", default=False, when="@10:", description="Build with MLIR support")
    variant(
        "libunwind",
        values=(
            "none",
            conditional("project", when="@:15"),
            conditional("runtime", when="+clang @6:"),
        ),
        default="runtime",
        description="Build the LLVM unwinder library"
        "either as a runtime (with just-build Clang) "
        "or as a project (with the compiler in use)",
    )
    variant(
        "polly",
        default=True,
        description="Build the LLVM polyhedral optimization plugin, only builds for 3.7.0+",
    )
    variant(
        "libcxx",
        values=(
            "none",
            conditional("project", when="@:15"),
            conditional("runtime", when="+clang @6:"),
        ),
        default="runtime",
        description="Build the LLVM C++ standard library "
        "either as a runtime (with just-build Clang) "
        "or as a project (with the compiler in use)",
    )

    variant("offload", default=True, when="@19:", description="Build the Offload subproject")
    conflicts("+offload", when="~clang")

    # The offload subproject requires lld:
    # https://github.com/llvm/llvm-project/commit/346792aafb483a53fb5e3274298d85bc2dde4a35
    conflicts("~lld", when="+offload")

    variant("libomptarget", default=True, description="Build the OpenMP offloading library")
    conflicts("+libomptarget", when="~clang")
    conflicts("+libomptarget", when="~offload @19:")
    for _p in ["darwin", "windows"]:
        conflicts("+libomptarget", when="platform={0}".format(_p))
    del _p

    variant(
        "libomptarget_debug",
        default=False,
        description="Allow debug output with the environment variable LIBOMPTARGET_DEBUG=1",
    )
    conflicts("+libomptarget_debug", when="~libomptarget")

    variant(
        "compiler-rt",
        values=(
            "none",
            conditional("project", when="+clang"),
            conditional("runtime", when="+clang @6:"),
        ),
        default="runtime",
        description="Build the LLVM compiler runtime, including sanitizers, "
        "either as a runtime (with just-build Clang) "
        "or as a project (with the compiler in use)",
    )
    variant(
        "gold",
        default=(sys.platform != "darwin"),
        description="Add support for LTO with the gold linker plugin",
    )
    variant("split_dwarf", default=False, description="Build with split dwarf information")
    variant(
        "llvm_dylib",
        default=True,
        description="Build a combined LLVM shared library with all components",
    )
    variant(
        "link_llvm_dylib",
        default=False,
        when="+llvm_dylib",
        description="Link LLVM tools against the LLVM shared library",
    )
    variant(
        "targets",
        default="all",
        description=(
            "What targets to build. Spack's target family is always added "
            "(e.g. X86 is automatically enabled when targeting znver2)."
        ),
        values=(
            "all",
            "none",
            "aarch64",
            "amdgpu",
            "arm",
            "avr",
            "bpf",
            "cppbackend",
            "hexagon",
            "lanai",
            "mips",
            "msp430",
            "nvptx",
            "powerpc",
            "riscv",
            "sparc",
            "systemz",
            "webassembly",
            "x86",
            "xcore",
        ),
        multi=True,
    )
    variant(
        "libomp_tsan",
        default=False,
        # Added in https://reviews.llvm.org/D13072
        # Removed in https://reviews.llvm.org/D103767
        when="@4:12",
        description="Build with OpenMP capable thread sanitizer",
    )
    variant(
        "openmp",
        values=("project", conditional("runtime", when="+clang @12:")),
        default="runtime",
        description="Build OpenMP either as a runtime (with just-build Clang) "
        "or as a project (with the compiler in use)",
    )
    variant(
        "code_signing",
        default=False,
        when="+lldb platform=darwin",
        description="Enable code-signing on macOS",
    )
    variant("python", default=False, description="Install python bindings")
    variant("lua", default=True, description="Enable lua scripting inside lldb")
    variant("version_suffix", default="none", description="Add a symbol suffix")
    variant(
        "shlib_symbol_version",
        default="none",
        description="Add shared library symbol version",
        when="@13:",
    )
    variant("z3", default=False, description="Use Z3 for the clang static analyzer")
    conflicts("+z3", when="@:7")
    conflicts("+z3", when="~clang")
    conflicts("+lua", when="@:10")
    conflicts("+lua", when="~lldb")
    # Python distutils were removed with 3.12 and are required to build LLVM <= 14
    conflicts("^python@3.12:", when="@:14")



    with when("@:10"):
        # Versions 10 and older cannot build runtimes with cmake@3.17:
        # See https://reviews.llvm.org/D77284
        for runtime in ["libunwind", "libcxx", "compiler-rt"]:
            depends_on("cmake@:3.16", type="build", when="{0}=runtime".format(runtime))
        del runtime
    depends_on("python@3.8:", when="@20: ~python", type="build")
    # Universal dependency

    # openmp dependencies

    # needs zstd cmake config file, which is not added when built with makefile.


    for _when_spec in ("+lldb+python", "+lldb+lua"):
            # 81fc5f7909a4ef5a8d4b5da2a10f77f7cb01ba63 fixed swig 4.1 support
            depends_on("swig@:4.0", when="@:15")

    # gold support, required for some features
    depends_on("binutils+gold+ld+plugins+headers", when="+gold")

    # Older LLVM do not build with newer compilers, and vice versa
    with when("@16:"):
        conflicts("%gcc@:7.0")
        conflicts("%clang@:4")
        conflicts("%apple-clang@:9")
    conflicts("%gcc@8:", when="@:5")
    conflicts("%gcc@:5.0", when="@8:")
    conflicts("%gcc@8.4:8.4.9", when="@12: target=aarch64:")

    # libcxx=project imposes compiler conflicts
    with when("libcxx=project"):
        for v, compiler_conflicts in {
            "@7:": {"clang": "@:3.4", "gcc": "@:4.6"},
            "@9:": {"clang": "@:3.4", "gcc": "@:4"},
            "@11:": {"clang": "@:3", "gcc": "@:4"},
            "@13:": {"clang": "@:10", "gcc": "@:10", "apple-clang": "@:11"},
            "@14:": {
                "clang": "@:11",
                "gcc": "@:10",
                "apple-clang": "@:11",
                "xlc": "@:17.0",
                "xlc_r": "@:17.0",
            },
            "@15:": {
                "clang": "@:12",
                "gcc": "@:11",
                "apple-clang": "@:12",
                "xlc": "@:17.0",
                "xlc_r": "@:17.0",
            },
            "@16:": {
                "clang": "@:13",
                "gcc": "@:11",
                "apple-clang": "@:13",
                "xlc": "@:17.0",
                "xlc_r": "@:17.0",
            },
        }.items():
            with when(v):
                for _name, _constraint in compiler_conflicts.items():
                    conflicts(f"%{_name}{_constraint}")
        del v, compiler_conflicts, _name, _constraint

    # libomptarget
    conflicts("+cuda", when="@15:")  # +cuda variant is obselete since LLVM 15
    conflicts(
        "targets=none",
        when="+libomptarget",
        msg="Non-host backends needed for offloading, set targets=all",
    )
    # See https://github.com/spack/spack/pull/32476#issuecomment-1573770361
    conflicts("~lld", when="+libomptarget")

    # cuda_arch value must be specified
    conflicts("cuda_arch=none", when="+cuda", msg="A value for cuda_arch must be specified.")

    # clang/test/Misc/target-invalid-cpu-note.c
    conflicts("cuda_arch=10")
    conflicts("cuda_arch=90", when="@:15")
    conflicts("cuda_arch=90a", when="@:17")

    # LLVM bug https://bugs.llvm.org/show_bug.cgi?id=48234
    # CMake bug: https://gitlab.kitware.com/cmake/cmake/-/issues/21469
    # Fixed in upstream versions of both
    conflicts("^cmake@3.19.0", when="@6:11.0.0")

    # Fix lld templates: https://bugs.freebsd.org/bugzilla/show_bug.cgi?id=230463
    patch(
        "https://raw.githubusercontent.com/freebsd/freebsd-ports/f8f9333d8e1e5a7a6b28c5ef0ca73785db06136e/devel/llvm50/files/lld/patch-tools_lld_ELF_Symbols.cpp",
        sha256="c81a50c1b6b78d359c0ce3b88914477f4f2a85b8dbfa7ac745b9e7eb4e53931b",
        when="@5+lld%clang@7:",
    )

    # Add missing include directives for the standard headers (the real need for the following
    # patches depends on the implementation of the standard C++ library, the headers, however, must
    # be included according to the standard, therefore, we apply the patches regardless of the
    # compiler and compiler version).
    #
    # fix missing ::size_t in 'llvm@4:5'
    # see comments in the patch file
    patch(
        "xray_buffer_queue-cstddef.patch",
        # we do not cover compiler-rt=runtime because it is not supported when @:5
        when="@4:5 compiler-rt=project",
    )
    #
    # see https://reviews.llvm.org/D64937
    # see https://github.com/spack/spack/issues/24270
    patch(
        "https://github.com/llvm/llvm-project/commit/b288d90b39f4b905c02092a9bfcfd6d78f99b191.patch?full_index=1",
        sha256="2028d52e1a39326bb48fb7463132bbfe7fb4fa18f1adfeea9c3ed0320ed49564",
        when="@8:9.0.0",
    )
    #
    # committed upstream without a review
    # see https://github.com/llvm/llvm-project/commit/b498303066a63a203d24f739b2d2e0e56dca70d1
    # see https://github.com/spack/spack/pull/28547
    patch(
        "https://github.com/llvm/llvm-project/commit/b498303066a63a203d24f739b2d2e0e56dca70d1.patch?full_index=1",
        sha256="514926d661635de47972c7d403c9c4669235aa51e22e56d44676d2a2709179b6",
        when="@8:11",
    )
    #
    # fix compilation against libstdc++13
    patch(
        "https://github.com/llvm/llvm-project/commit/1b4fdf18bc2aaa2d46bf072475dd9cbcd44a9fee.patch?full_index=1",
        sha256="82481418766b4b949ea808d956ff3800b9a241a576370114862428bb0e25ee1f",
        when="@14:15",
    )

    # missing <cstdint> include
    patch(
        "https://github.com/llvm/llvm-project/commit/ff1681ddb303223973653f7f5f3f3435b48a1983.patch?full_index=1",
        sha256="c6ca6b925f150e8644ce756023797b7f94c9619c62507231f979edab1c09af78",
        when="@6:13",
    )
    # fix building of older versions of llvm with newer versions of glibc
    for compiler_rt_as in ["project", "runtime"]:
        with when("compiler-rt={0}".format(compiler_rt_as)):
            # sys/ustat.h has been removed in favour of statfs from glibc-2.28
            # see https://reviews.llvm.org/D47281
            patch(
                "https://github.com/llvm/llvm-project/commit/383fe5c8668f63ef21c646b43f48da9fa41aa100.patch?full_index=1",
                sha256="66f01ac1769a6815aba09d6f4347ac1744f77f82ec9578a1158b24daca7a89e6",
                when="@4:6.0.0",
            )
            # fix sanitizer-common build with glibc 2.31
            # see https://reviews.llvm.org/D70662
            patch("sanitizer-ipc_perm_mode.patch", when="@5:9")
    del compiler_rt_as

    # Backport from llvm upstream gcc ppc const expr long double issue
    # see https://bugs.llvm.org/show_bug.cgi?id=39696
    # This fix was initially committed (3bf63cf3b366) for the 9.0 release
    # but was then broken (0583d9ea8d5e) prior to the 9.0 release and
    # eventually unbroken (d9a42ec98adc) for the 11.0 release.  The first
    # patch backports the original correct fix to previous releases.  The
    # second patch backports the un-breaking of the original fix.
    for libcxx_as in ["project", "runtime"]:
        with when("libcxx={0}".format(libcxx_as)):
            patch(
                "https://github.com/llvm/llvm-project/commit/3bf63cf3b366d3a57cf5cbad4112a6abf6c0c3b1.patch?full_index=1",
                sha256="e56489a4bcf3c3636e206adca366bfcda2722ad81a5fa9a0360faed63933191a",
                when="@6:8",
            )
            patch(
                "https://github.com/llvm/llvm-project/commit/d9a42ec98adcb1ebc0c3837715df4e5a50c7ccc0.patch?full_index=1",
                sha256="50bfc4e82c02bb5b7739990f363d99b1e43d5d11a5104f6aabbc303ebce6fbe3",
                when="@9:10",
            )
    del libcxx_as

    # Backport from llvm to fix issues related to Python 3.7
    # see https://bugs.llvm.org/show_bug.cgi?id=38233
    patch(
        "https://github.com/llvm/llvm-project/commit/5457b426f5e15a29c0acc8af1a476132f8be2a36.patch?full_index=1",
        sha256="7a1e4aa80760167807255c3e3121b1281bfcf532396b2d8fb3dce021f3f18758",
        when="@4:6+python+lldb ^python@3.7:",
    )

    # fix building on SUSE (with panel.h being in /usr/include/ncurses/)
    # see https://reviews.llvm.org/D85219
    # see https://github.com/spack/spack/issues/19625
    patch(
        "https://github.com/llvm/llvm-project/commit/c952ec15d38843b69e22dfd7b0665304a0459f9f.patch?full_index=1",
        sha256="66932ba31b5bf8808ea112e42cfd79b2480a4936e711771c06ce851eac429b2c",
        when="@10:11+lldb",
    )

    # honor Python2_EXECUTABLE and Python3_EXECUTABLE when they are passed to cmake
    # see https://reviews.llvm.org/D91536
    patch(
        "https://github.com/llvm/llvm-project/commit/16de50895e96adbe261a5ce2498366bda7b3fccd.patch?full_index=1",
        sha256="0e121ed460aa6e117f9f5f339d597a96c0fe4f97dc2209aba47b43ffc831ea24",
        # The patch is applicable only starting version 7.0.0 (the older version might require a
        # different patch addressing https://github.com/spack/spack/issues/19908). It looks like
        # the patched function is used only if both compiler-rt and libcxx are enabled but we keep
        # it simple:
        when="@7:11",
    )

    # Workaround for issue https://github.com/spack/spack/issues/18197
    patch("llvm7_intel.patch", when="@7 %intel@18.0.2,19.0.0:19.1.99")

    # Remove cyclades support to build against newer kernel headers
    # https://reviews.llvm.org/D102059
    patch(
        "https://github.com/llvm/llvm-project/commit/68d5235cb58f988c71b403334cd9482d663841ab.patch?full_index=1",
        sha256="742501723642675075e617f3c38339961b2c7b6fd8290dbffc52239ab0783317",
        when="@10:12.0.0",
    )
    # The patch above is not applicable when "@:9" due to the file renaming and reformatting. The
    # following patch is applicable starting at least version 5.0.0, the oldest we try to support.
    patch("no_cyclades9.patch", when="@5:9")

    with when("+libomptarget"):
        # libomptarget makes use of multithreading via the standard C++ library (e.g.
        # std::call_once), which, depending on the platform and the implementation of the standard
        # library, might or might not require linking to libpthread (note that the failure might
        #  least for newer versions (the solution must work with both openmp=runtime and
        #  openmp=project)
        patch("llvm13-14-thread.patch", when="@13:14")
        patch("llvm15-thread.patch", when="@15")

    # avoid build failed with Fujitsu compiler
    patch("llvm13-fujitsu.patch", when="@13 %fj")

    # avoid build failed with Fujitsu compiler since llvm17
    patch("llvm17-fujitsu.patch", when="@17: %fj")

    # patch for missing hwloc.h include for libompd
    # see https://reviews.llvm.org/D123888


    # fix detection of LLDB_PYTHON_EXE_RELATIVE_PATH
    # see https://reviews.llvm.org/D133513
    # TODO: the patch is not applicable after https://reviews.llvm.org/D141042 but it is not clear
    #  yet whether we need a version of it for when="@16:"

    # https://reviews.llvm.org/D127975


    # https://github.com/llvm/llvm-project/issues/156679
    @when("@14:17")
    def patch(self):
        filter_file(
            r"${TERMINFO_LIB}",
            r"${Terminfo_LIBRARIES}",
            "lldb/source/Core/CMakeLists.txt",
            string=True,
        )

    clang_and_friends = "(?:clang|flang|flang-new)"

    compiler_version_regex = (
        # Normal clang compiler versions are left as-is
        rf"{clang_and_friends} version ([^ )\n]+)-svn[~.\w\d-]*|"
        # Don't include hyphenated patch numbers in the version
        # (see https://github.com/spack/spack/pull/14365 for details)
        rf"{clang_and_friends} version ([^ )\n]+?)-[~.\w\d-]*|"
        rf"{clang_and_friends} version ([^ )\n]+)|"
        # LLDB
        r"lldb version ([^ )\n]+)|"
        # LLD
        r"LLD ([^ )\n]+) \(compatible with GNU linkers\)"
    )
    fortran_names = ["flang", "flang-new"]

    @property
    def supported_languages(self):
        languages = []
        if self.spec.satisfies("+clang"):
            languages.extend(["c", "cxx"])
        if self.spec.satisfies("+flang"):
            languages.append("fortran")
        return languages

    @classproperty
    def executables(cls):
        return super().executables + [r"^ld\.lld(-\d+)?$", r"^lldb(-\d+)?$"]

    @classmethod
    def determine_version(cls, exe):
        try:
            compiler = Executable(exe)
            output = compiler(cls.compiler_version_argument, output=str, error=str)
            if "Apple" in output:
                return None
            if "AMD" in output:
                return None
            match = re.search(cls.compiler_version_regex, output)
            if match:
                return match.group(match.lastindex)
        except ProcessError:
            pass
        except Exception as e:
            tty.debug(e)

        return None

    @classmethod
    def determine_variants(cls, exes, version_str):
        # Do not need to reuse more general logic from CompilerPackage
        # because LLVM has kindly named compilers

        # Map between exectuable name, variant name, and compiler language.
        # The ordering of this list is the ordering of the returned variants.
        exe_variant_lang = [
            ("clang++", "clang", "cxx"),
            ("clang", "clang", "c"),
            ("flang", "flang", "fortran"),
            ("ld.lld", "lld", None),
            ("lldb", "lldb", None),
        ]

        variants = set()
        compilers = {}

        # Prefer shorter pathnames by sorting with len and using setdefault
        for exe_path in sorted(exes, key=len):
            name = os.path.basename(exe_path)
            for exe, var, lang in exe_variant_lang:
                # NOTE: since "amdclang++" is "clang", we use `in` rather than `startswith`
                if exe in name:
                    compilers.setdefault(lang, exe_path)
                    variants.add(var)
                    break

        # Remove executables that aren't compilers
        compilers.pop(None, None)

        # Convert
        added_variant = set()
        variant_strings = []
        for _, var, _ in exe_variant_lang:
            # Prevent double-clang variant
            if var in added_variant:
                continue
            added_variant.add(var)

            # Add variant string
            prefix = "+" if var in variants else "~"
            variant_strings.append(prefix + var)

        return "".join(variant_strings), {"compilers": compilers}

    @classmethod
    def validate_detected_spec(cls, spec, extra_attributes):
        # For LLVM 'compilers' is a mandatory attribute
        msg = 'the extra attribute "compilers" must be set for the detected spec "{0}"'.format(
            spec
        )
        assert "compilers" in extra_attributes, msg
        compilers = extra_attributes["compilers"]
        for key in ("c", "cxx"):
            msg = "{0} compiler not found for {1}"
            assert key in compilers, msg.format(key, spec)

    def _cc_path(self):
        if self.spec.satisfies("+clang"):
            return os.path.join(self.spec.prefix.bin, "clang")
        return None

    def _cxx_path(self):
        if self.spec.satisfies("+clang"):
            return os.path.join(self.spec.prefix.bin, "clang++")
        return None

    def _fortran_path(self):
        if self.spec.satisfies("+flang"):
            return os.path.join(self.spec.prefix.bin, "flang")
        return None

    debug_flags = [
        "-gcodeview",
        "-gdwarf-2",
        "-gdwarf-3",
        "-gdwarf-4",
        "-gdwarf-5",
        "-gline-tables-only",
        "-gmodules",
        "-g",
    ]

    opt_flags = ["-O0", "-O1", "-O2", "-O3", "-Ofast", "-Os", "-Oz", "-Og", "-O", "-O4"]

    compiler_wrapper_link_paths = {
        "c": os.path.join("clang", "clang"),
        "cxx": os.path.join("clang", "clang++"),
        "fortran": os.path.join("clang", "flang"),
    }

    implicit_rpath_libs = ["libclang"]

    def _standard_flag(self, *, language, standard):
        flags = {
            "cxx": {
                "11": [("@3.3:", "-std=c++11")],
                "14": [("@3.5:", "-std=c++14")],
                "17": [("@3.5:4", "-std=c++1z"), ("@5:", "-std=c++17")],
                "20": [("@5:10", "-std=c++2a"), ("@11:", "-std=c++20")],
                "23": [("@12:16", "-std=c++2b"), ("@17:", "-std=c++23")],
            },
            "c": {
                "99": [("@:", "-std=c99")],
                "11": [("@3.1:", "-std=c11")],
                "17": [("@6:", "-std=c17")],
                "23": [("@9:17", "-std=c2x"), ("@18:", "-std=c23")],
            },
        }
        for condition, flag in flags[language][standard]:
            if self.spec.satisfies(condition):
                return flag
        else:
            raise RuntimeError(
                f"{self.spec} does not support the '{standard}' standard "
                f"for the '{language}' language"
            )

    def archspec_name(self):
        return "clang"

    @property
    def libs(self):
        return LibraryList(self.llvm_config("--libfiles", "all", result="list"))

    @run_before("cmake")
    def codesign_check(self):
        if self.spec.satisfies("+code_signing"):
            codesign = which("codesign")
            mkdir("tmp")
            llvm_check_file = join_path("tmp", "llvm_check")
            copy("/usr/bin/false", llvm_check_file)
            try:
                codesign("-f", "-s", "lldb_codesign", "--dryrun", llvm_check_file)

            except ProcessError:
                # Newer LLVM versions have a simple script that sets up
                # automatically when run with sudo priviliges
                setup = Executable("./lldb/scripts/macos-setup-codesign.sh")
    def setup_run_environment(self, env: EnvironmentModifications) -> None:
        if self.spec.satisfies("+clang"):
            env.set("CC", join_path(self.spec.prefix.bin, "clang"))
            env.set("CXX", join_path(self.spec.prefix.bin, "clang++"))
        if self.spec.satisfies("+flang"):
            env.set("FC", join_path(self.spec.prefix.bin, "flang"))
            env.set("F77", join_path(self.spec.prefix.bin, "flang"))

    root_cmakelists_dir = "llvm"

    def cmake_args(self):
        spec = self.spec
        define = self.define
        from_variant = self.define_from_variant

        cmake_args = [
            define("LLVM_REQUIRES_RTTI", True),
            define("LLVM_ENABLE_RTTI", True),
            define("LLVM_ENABLE_LIBXML2", False),
            define("CLANG_DEFAULT_OPENMP_RUNTIME", "libomp"),
            define("LIBOMP_USE_HWLOC", True),
            define("LIBOMP_HWLOC_INSTALL_DIR", spec["hwloc"].prefix),
            from_variant("LLVM_ENABLE_ZSTD", "zstd"),
        ]

        # Flang does not support exceptions from core llvm.
        # LLVM_ENABLE_EH=True when building flang will soon
        # fail (with changes at the llvm-project level).
        # Only enable exceptions in LLVM if we are *not*
