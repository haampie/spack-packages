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

    variant("scotch", default=True, description="With scotch/ptscotch decomposition")
    variant("zoltan", default=False, description="With zoltan renumbering")
    variant("mgridgen", default=False, description="With mgridgen support")
    variant(
        "paraview", default=False, description="Build paraview plugins and runtime post-processing"
    )
    variant("vtk", default=False, description="With VTK runTimePostProcessing")


    # After 1712, could suggest openmpi+thread_multiple for collated output
    # conflicts('^openmpi~thread_multiple', when='@1712:')


    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # Earlier versions of OpenFOAM may not work with CGAL 5.6. I do
    # not know which OpenFOAM added support for 5.x and conservatively
    # use 2312 in the check.
    # cgal@6 needs c++17, but until v2412 OpenFOAM forced c++14
    depends_on("cgal@:4", when="@:2306")

    # The flex restriction is ONLY to deal with a spec resolution clash
    # introduced by the restriction within scotch!
    depends_on("flex@:2.6.1,2.6.4:")

    # mgridgen is statically linked
    # 'paraview+plugins' but that resolves poorly.
    # 1612 plugins need older paraview
    depends_on("paraview@:5.0.1", when="@1612+paraview")

    # Icx only support from v2106 onwards

    # General patches
    assets = []  # type: List[str]
    # Version-specific patches
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

# -----------------------------------------------------------------------------
