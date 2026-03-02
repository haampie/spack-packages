# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
# Author: Mark Olesen <mark.olesen@esi-group.com>
#
# Legal Notice
# ------------
# OPENFOAM is a trademark owned by OpenCFD Ltd
# (producer and distributor of the OpenFOAM software via www.openfoam.com).
# The trademark information must remain visible and unadulterated in this
# file and via the "spack info" and comply with the term set by
# http://openfoam.com/legal/trademark-policy.php
#
# This file is not part of OpenFOAM, nor does it constitute a component of an
# OpenFOAM distribution.
#
##############################################################################
#
# Notes
# - mpi handling: WM_MPLIB=USERMPI and use spack to generate mplibUSERMPI
#   wmake rules.
#
# - Resolution of flex, zlib needs more attention (within OpenFOAM)
# - +paraview:
#   depends_on should just be 'paraview+plugins' but that resolves poorly.
#   Workaround: use preferred variants "+plugins +qt"
#       packages:
#           paraview:
#               variants: +plugins +qt
#   in ~/.spack/packages.yaml
#
# Known issues
# - Combining +zoltan with +int64 has not been tested, but probably won't work.
# - Combining +mgridgen with +int64 or +float32 probably won't work.
#
# The spack 'develop' version of openfoam retains the upstream
# WM_PROJECT_VERSION=com naming internally.
#
##############################################################################
import glob
import os
import re

from spack_repo.builtin.build_systems.generic import Package
from spack_repo.builtin.packages.boost.package import Boost

from spack.package import *

# Not the nice way of doing things, but is a start for refactoring
__all__ = [
    "add_extra_files",
    "write_environ",
    "rewrite_environ_files",
    "mplib_content",
    "foam_add_path",
    "foam_add_lib",
    "OpenfoamArch",
]


def foam_add_lib(*args):
    """A string with args prepended to 'LD_LIBRARY_PATH'"""
    return '"' + ":".join(args) + ':${LD_LIBRARY_PATH}"'


def pkglib(package, pre=None):
    """Get lib64 or lib from package prefix.

    Optional parameter 'pre' to provide alternative prefix
    """
    libdir = package.prefix.lib64
    if not os.path.isdir(libdir):
        libdir = package.prefix.lib
    if pre:
        return join_path(pre, os.path.basename(libdir))
    else:
        return libdir


def mplib_content(spec, pre=None):
    """The mpi settings (from spack) for the OpenFOAM wmake includes, which
    allows later reuse within OpenFOAM.

    Optional parameter 'pre' to provide alternative prefix for
    bin and lib directories.
    """
    mpi_spec = spec["mpi"]
    bin = mpi_spec.prefix.bin
    inc = mpi_spec.headers.directories[0]  # Currently only need first one
    lib = pkglib(mpi_spec)

    libname = "mpi"
    if "mpich" in mpi_spec.name:
        libname = "mpich"

    if pre:
        bin = join_path(pre, os.path.basename(bin))
        inc = join_path(pre, os.path.basename(inc))
        lib = join_path(pre, os.path.basename(lib))
    else:
        pre = mpi_spec.prefix

    info = {
        "name": "{0}-{1}".format(mpi_spec.name, mpi_spec.version),
        "prefix": pre,
        "include": inc,
        "bindir": bin,
        "libdir": lib,
        "FLAGS": "-DOMPI_SKIP_MPICXX -DMPICH_SKIP_MPICXX",
        "PINC": "-I{0}".format(inc),
        "PLIBS": "-L{0} -l{1}".format(lib, libname),
    }
    return info


def submodules(package):
    submodules = []
    if package is not None and package.spec.satisfies("plugins=avalanche"):
        submodules.append("plugins/avalanche")
    if package is not None and package.spec.satisfies("plugins=cfmesh"):
        submodules.append("plugins/cfmesh")
    return submodules


# -----------------------------------------------------------------------------


class Openfoam(Package):
    """OpenFOAM is a GPL-opensource C++ CFD-toolbox.
    This offering is supported by OpenCFD Ltd,
    producer and distributor of the OpenFOAM software via www.openfoam.com,
    and owner of the OPENFOAM trademark.
    OpenCFD Ltd has been developing and releasing OpenFOAM since its debut
    in 2004.
    """

    homepage = "https://www.openfoam.com/"
    url = "https://sourceforge.net/projects/openfoam/files/v1906/OpenFOAM-v1906.tgz"
    git = "https://gitlab.com/openfoam/core/openfoam.git"
    list_url = "https://sourceforge.net/projects/openfoam/files/"
    list_depth = 2


    version("develop", branch="develop", submodules=True)
    version("master", branch="master", submodules=True)
    version(
        "2512",
        tag="OpenFOAM-v2512",
        commit="87ed40d256d22ea38fcc648dfc82a22162427b18",
        submodules=submodules,
    )
    version("2506", sha256="63d26f48ae7ee9a7806a0ceb339ef8a0ba485a4714d54fbfb31e78e1a4849965")
    version(
        "2212_230612", sha256="604cd731173ec2a3645c838cf2468fae050a35c6340e2ca7c157699899d904c0"
    )
    version("2212", sha256="0a3ddbfea9abca04c3a811e72fcbb184c6b1f92c295461e63b231f1a97e96476")
    version(
        "2106_211215", sha256="08c0d0b90b43505693ff8838e827f09e14ec9fb475956ef53cc2206c736277b1"
    )
    version("2012", sha256="3d6e39e39e7ae61d321fbc6db6c3748e6e5e1c4886454207a7f1a7321469e65a")
    version(
        "2006_220610", sha256="b8e9801c304f3fdf512ed8840093bf3f348fb8701121c88f3febd45e3826cb22"
    )
    version(
        "2006_201012", sha256="9afb7eee072bfddcf7f3e58420c93463027db2394997ac4c3b87a8b07c707fb0"
    )
    version("2006", sha256="30c6376d6f403985fc2ab381d364522d1420dd58a42cb270d2ad86f8af227edc")
    version(
        "1906_200312", sha256="f75645151ed5d8c5da592d307480979fe580a25627cc0c9718ef370211577594"
    )
    version(
        "1906_191103", sha256="631a7fcd926ccbcdef0ab737a9dc55e58d6bedae2f3acaa041ea679db6c9303b"
    )
    version("1906", sha256="bee03c4b1da0d2c9f98eb469eeffbce3a8614728ef8e87f664042a7490976537")
    version(
        "1812_200312", sha256="925d2877c12740fab177a30fdcaa8899c262c15b90225f9c29d18a2d97532de0"
    )
    version("1612", sha256="2909c43506a68e1f23efd0ca6186a6948ae0fc8fe1e39c78cc23ef0d69f3569d")

    variant("int64", default=False, description="With 64-bit labels")
    variant("knl", default=False, description="Use KNL compiler settings")
    variant("kahip", default=False, description="With kahip decomposition")
    variant("metis", default=False, description="With metis decomposition")
    variant("scotch", default=True, description="With scotch/ptscotch decomposition")
    variant("zoltan", default=False, description="With zoltan renumbering")
    variant("mgridgen", default=False, description="With mgridgen support")
    variant(
        "paraview", default=False, description="Build paraview plugins and runtime post-processing"
    )
    variant("vtk", default=False, description="With VTK runTimePostProcessing")

    # but particular mixes of mpi versions and InfiniBand may not work so well
    # conflicts('^openmpi~thread_multiple', when='@1712:')


    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference

    # Earlier versions of OpenFOAM may not work with CGAL 5.6. I do
    # not know which OpenFOAM added support for 5.x and conservatively
    # use 2312 in the check.
    # cgal@6 needs c++17, but until v2412 OpenFOAM forced c++14

    # The flex restriction is ONLY to deal with a spec resolution clash
    # introduced by the restriction within scotch!
    depends_on("flex@:2.6.1,2.6.4:")
    depends_on("cmake", type="build")

    # Require scotch with ptscotch - corresponds to standard OpenFOAM setup
    depends_on("scotch~metis+mpi~int64", when="+scotch~int64")
    depends_on("scotch~metis+mpi+int64", when="+scotch+int64")
    depends_on("kahip", when="+kahip")
    depends_on("metis@5:", when="+metis")
    depends_on("metis+int64", when="+metis+int64")
    # mgridgen is statically linked
    depends_on("parmgridgen", when="+mgridgen", type="build")
    depends_on("zoltan", when="+zoltan")
    depends_on("vtk", when="+vtk")
    depends_on("adios2~fortran", when="@1912:")

    # For OpenFOAM plugins and run-time post-processing this should just be
    # 'paraview+plugins' but that resolves poorly.
    #   ~/.spack/packages.yaml

    # 1706 ok with newer paraview but avoid pv-5.2, pv-5.3 readers
    depends_on("paraview@5.4:", when="@1706:+paraview")
    # Icx only support from v2106 onwards

    # General patches
    common = ["spack-Allwmake", "README-spack"]
    assets = []  # type: List[str]

    # kahip patch (wmake)
    # Fix: missing std::array include (searchable sphere)

    # Some user config settings
    # default: 'compile-option': '-spack',
    # default: 'mplib': 'USERMPI',  # User-defined mpi for spack
    config = {
        # Add links into bin/, lib/ (eg, for other applications)
        "link": False
    }

    # The openfoam architecture, compiler information etc
    _foam_arch = None

    # Content for etc/prefs.{csh,sh}
    etc_prefs = {}  # type: Dict[str,str]

    # Content for etc/config.{csh,sh}/ files
    etc_config = {}  # type: Dict[str,str]

    phases = ["configure", "build", "install"]
    build_script = "./spack-Allwmake"  # From patch() method.

    #
    # - End of definitions / setup -
    #

    def url_for_version(self, version):
        """Handles locations for patched and unpatched versions.
        Patched version (eg '1906_191103') are located in the
        corresponding unpatched directories (eg '1906').
        Older versions (eg, v1612+) had additional '+' in naming
        """
        if version <= Version("1612"):
            fmt = "v{0}+/OpenFOAM-v{1}+.tgz"
        else:
            fmt = "v{0}/OpenFOAM-v{1}.tgz"
        return self.list_url + fmt.format(version.up_to(1), version)

    def setup_minimal_environment(self, env: EnvironmentModifications):
        """Sets a minimal openfoam environment."""
        tty.info("OpenFOAM minimal env {0}".format(self.prefix))
        env.set("FOAM_PROJECT_DIR", self.projectdir)
        env.set("WM_PROJECT_DIR", self.projectdir)
        for d in ["wmake", self.archbin]:  # bin added automatically
            env.prepend_path("PATH", join_path(self.projectdir, d))

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        """Sets the build environment (prior to unpacking the sources)."""
        pass

    def setup_run_environment(self, env: EnvironmentModifications) -> None:
        """Sets the run environment (post-installation).
        The environment comes from running:

        .. code-block:: console

           $ . $WM_PROJECT_DIR/etc/bashrc
        """

        bashrc = join_path(self.projectdir, "etc", "bashrc")
        minimal = True
        if os.path.isfile(bashrc):
            # post-install: source the installed bashrc
            try:
                mods = EnvironmentModifications.from_sourcing_file(
                    bashrc,
                    clean=True,  # Remove duplicate entries
                    blacklist=[  # Blacklist these
                        # Inadvertent changes
                        # -------------------
                        "PS1",  # Leave untouched
                        "MANPATH",  # Leave untouched
                        # Unneeded bits
                        # -------------
                        # 'FOAM_SETTINGS',  # Do not use with modules
                        # 'FOAM_INST_DIR',  # Old
                        # 'FOAM_(APP|ETC|SRC|SOLVERS|UTILITIES)',
                        # 'FOAM_TUTORIALS', # May be useful
                        # 'WM_OSTYPE',      # Purely optional value
                        # Third-party cruft - only used for orig compilation
                        # -----------------
                        "[A-Z].*_ARCH_PATH",
                        # '(KAHIP|METIS|SCOTCH)_VERSION',
                        # User-specific
                        # -------------
                        "FOAM_RUN",
                        "(FOAM|WM)_.*USER_.*",
                    ],
                    whitelist=[
                        "MPI_ARCH_PATH"
                    ],  # Whitelist these  # Can be required for compilation
                )

                env.extend(mods)
                minimal = False
                tty.debug("OpenFOAM bashrc env: {0}".format(bashrc))
            except Exception:
                minimal = True

        if minimal:
            # pre-build or minimal environment
            self.setup_minimal_environment(env)

    def setup_dependent_build_environment(
        self, env: EnvironmentModifications, dependent_spec: Spec
    ) -> None:
        """Use full OpenFOAM environment when building.
        Mirror WM_PROJECT_DIR value as FOAM_PROJECT_DIR to avoid
        masking the normal OpenFOAM cleanup of previous versions.
        """
        self.setup_run_environment(env)
        env.set("FOAM_PROJECT_DIR", self.projectdir)

    def setup_dependent_run_environment(
        self, env: EnvironmentModifications, dependent_spec: Spec
    ) -> None:
        """Use full OpenFOAM environment when running.
        Mirror WM_PROJECT_DIR value as FOAM_PROJECT_DIR to avoid
        masking the normal OpenFOAM cleanup of previous versions.
        """
        self.setup_run_environment(env)
        env.set("FOAM_PROJECT_DIR", self.projectdir)

    @property
    def projectdir(self):
        """Absolute location of project directory: WM_PROJECT_DIR/"""
        return self.prefix  # <- install directly under prefix

    @property
    def foam_arch(self):
        if not self._foam_arch:
            self._foam_arch = OpenfoamArch(self.spec, **self.config)
        return self._foam_arch

    @property
    def archbin(self):
        """Relative location of architecture-specific executables"""
        return join_path("platforms", self.foam_arch, "bin")

    @property
    def archlib(self):
        """Relative location of architecture-specific libraries"""
        return join_path("platforms", self.foam_arch, "lib")

    def patch(self):
        """Adjust OpenFOAM build for spack.
        Where needed, apply filter as an alternative to normal patching."""
        add_extra_files(self, self.common, self.assets)

    @when("@:1806")
    def patch(self):
        """Adjust OpenFOAM build for spack.
        Where needed, apply filter as an alternative to normal patching."""
        add_extra_files(self, self.common, self.assets)

        # Prior to 1812, required OpenFOAM-v{VER} directory when sourcing
        projdir = "OpenFOAM-v{0}".format(self.version)
        if not os.path.exists(join_path(self.stage.path, projdir)):
            tty.info("Added directory link {0}".format(projdir))
            symlink(
                os.path.relpath(self.stage.source_path, self.stage.path),
                join_path(self.stage.path, projdir),
            )

        # Avoid WM_PROJECT_INST_DIR for ThirdParty
        # This modification is non-critical
        edits = {
            "WM_THIRD_PARTY_DIR": r"$WM_PROJECT_DIR/ThirdParty  #SPACK: No separate third-party"
        }
        rewrite_environ_files(  # etc/{bashrc,cshrc}
            edits, posix=join_path("etc", "bashrc"), cshell=join_path("etc", "cshrc")
        )

        # The following filtering is non-critical.
        # It simply prevents 'site' dirs at the wrong level
        # (likely non-existent anyhow) from being added to
        # PATH, LD_LIBRARY_PATH.
        for rcdir in ["config.sh", "config.csh"]:
            rcfile = join_path("etc", rcdir, "settings")
            if os.path.isfile(rcfile):
                filter_file("WM_PROJECT_INST_DIR/", "WM_PROJECT_DIR/", rcfile, backup=False)

    # Executables like decomposePar require interface libraries for optional dependencies, but if
    # the dependency is missing, an dummy library is used and put in lib/dummy. Allow this until
    # the https://gitlab.com/openfoam/core/openfoam/-/issues/3283 is resolved.
    unresolved_libraries = [
        "libkahipDecomp.so",
        "libmetisDecomp.so",
        "libMGridGen.so",
        "libPstream.so",
        "libptscotchDecomp.so",
        "libscotchDecomp.so",
    ]


# -----------------------------------------------------------------------------


class OpenfoamArch:
    """OpenfoamArch represents architecture/compiler settings for OpenFOAM.
    The string representation is WM_OPTIONS.

    Keywords
        label-size=[True]   supports int32/int64
        compile-option[=-spack]
        mplib[=USERMPI]
    """

    #: Map spack compiler names to OpenFOAM compiler names
    #  By default, simply capitalize the first letter
    compiler_mapping = {
        "aocc": "Amd",
        "fj": "Fujitsu",
        "intel": "Icc",
        "intel-oneapi-compilers": "Icx",
    }

    def has_rule(self, projdir):
        """Verify that a wmake/rules/ compiler rule exists in the project."""
        # Insist on a wmake rule for this architecture/compiler combination
        rule_dir = self._rule_directory(projdir)

        if not os.path.isdir(rule_dir):
            raise InstallError("No wmake rule for {0} {1}".format(self.arch, self.compiler))
        return True

    def _rule_add_rpath(self, rpath, src, dst):
        """Create {c,c++}-spack rules in the specified project directory.
        The compiler rules are based on the respective {cflags,cxxflags}-Opt or
        {c,c++}Opt rules with additional rpath information for the OpenFOAM libraries.

        The '-spack' rules channel spack information into OpenFOAM wmake
        rules with minimal modification to OpenFOAM.
        The rpath is used for the installed libpath (continue to use
        LD_LIBRARY_PATH for values during the build).
        """
        # Note: the 'c' rules normally don't need rpath, since they are just
        # used for some statically linked wmake tools, but left in anyhow.

        ok = os.path.isfile(src)

        if ok:
            with open(src, "r") as infile:
                with open(dst, "w") as outfile:
                    for line in infile:
                        line = line.rstrip()
                        outfile.write(line)
                        if re.match(r"^\S+DBUG\s*:?=", line):
                            outfile.write(" ")
                            outfile.write(rpath)
                        elif re.match(r"^\S+OPT\s*:?=", line):
                            if self.arch_option:
                                outfile.write(" ")
                                outfile.write(self.arch_option)
                        outfile.write("\n")
        return ok

    def create_rules(self, projdir, foam_pkg):
        """Create {c,c++}-spack and mplib{USERMPI} rules in the
        specified project directory.
        Uses General/common/{c,c++}Opt or arch-specific {c,c++}Opt rules,
        but with additional rpath information for the OpenFOAM libraries.

        The '-spack' rules channel spack information into OpenFOAM wmake
        rules with minimal modification to OpenFOAM.
        The rpath is used for the installed libpath (continue to use
        LD_LIBRARY_PATH for values during the build).
        """
        # Note: the 'c' rules normally don't need rpath, since they are just
        # used for some statically linked wmake tools, but left in anyhow.

        # rpath for installed OpenFOAM libraries
        rpath = "{0}{1}".format(
            foam_pkg.compiler.cxx_rpath_arg, join_path(foam_pkg.projectdir, foam_pkg.archlib)
        )

        user_mpi = mplib_content(foam_pkg.spec)
        rule_dir = self._rule_directory(projdir)
        comm_dir = self._rule_directory(projdir, False, True)

        # Compiler: copy existing {c,c++}Opt or General/common/{c,c++}Opt
        # and modify '*DBUG' value to include rpath

        for lang in ["c", "c++"]:
            gen = join_path(comm_dir, "{0}Opt".format(lang))
            src = join_path(rule_dir, "{0}Opt".format(lang))
            dst = join_path(rule_dir, "{0}{1}".format(lang, self.compile_option))

            if not self._rule_add_rpath(rpath, src, dst):
                self._rule_add_rpath(rpath, gen, dst)

        with working_dir(rule_dir):
            # MPI rules
            for mplib in ["mplibUSERMPI"]:
                with open(mplib, "w") as out:
                    out.write(
                        """# MPI from spack ({name})\n
PFLAGS  = {FLAGS}
PINC    = {PINC}
PLIBS   = {PLIBS}
#-------
""".format(
                            **user_mpi
                        )
                    )


# -----------------------------------------------------------------------------
