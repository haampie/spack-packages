# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

# Import re module to use regular expression
import re

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class VisitSilo(CMakePackage):
    """This is the Silo Plug-In for VisIt.
    It can be installed after VisIt is installed along SILO library.
    It is made as an extension to VisIt that can be activated or as an environment
    with a view: ~/.visit
    Complete explanation at:
    https://github.com/spack/spack/pull/22907#issuecomment-824218296
    """

    # These settings are exactly those of VisIt
    homepage = "https://wci.llnl.gov/simulation/computer-codes/visit/"
    git = "https://github.com/visit-dav/visit.git"
    url = "https://github.com/visit-dav/visit/releases/download/v3.1.1/visit3.1.1.tar.gz"


    # Here we provide a local file that contains only the plugin in a flat directory
    # Below we copy the VisIt paths:

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("cmake", type="build")
    depends_on("silo")
    depends_on("visit")

    extends("visit")

    build_targets = ["VERBOSE=1"]
    phases = ["cmake", "build"]
    extname = "Silo"

    @property
    def root_cmakelists_dir(self):
        if "@local" not in self.spec:
            return join_path("src", "databases", self.extname)
        else:
            return "."

    @property
    def build_directory(self):
        return self.root_cmakelists_dir

    @run_before("cmake")
    def run_xml2cmake(self):
        visit = self.spec["visit"]
        args = ["-v", str(visit.version), "-clobber", "-public", self.extname + ".xml"]
        with working_dir(self.root_cmakelists_dir):
            # Regenerate the public cmake files
            if os.path.exists("CMakeLists.txt"):
                os.unlink("CMakeLists.txt")
            which("xml2cmake")(*args)
            # spack extension activate : alter VISIT_PLUGIN_DIR ;
            # xml2cmake should have set it to visit prefix but it can
            # happen the directory is an alias.
            # In that case we match version/smth/plugins.
            mstr = None
            mstr1 = r"^SET[(]VISIT_PLUGIN_DIR\s+\"{0}(.+)\"[)]".format(visit.prefix)
            mstr2 = r"^SET[(]VISIT_PLUGIN_DIR\s+\".+({0}.+?{1})\"[)]".format(
                join_path(os.sep, visit.version, ""), join_path(os.sep, "plugins")
            )
            with open("CMakeLists.txt", "r") as file:
                for line in file:
                    if re.search(mstr1, line):
                        mstr = mstr1
                    elif re.search(mstr2, line):
                        mstr = mstr2
            if mstr is not None:
                filter_file(
                    mstr, r'SET(VISIT_PLUGIN_DIR "{0}\1")'.format(prefix), "CMakeLists.txt"
                )

    def cmake_args(self):
        silo = self.spec["silo"]
        args = [
            "-DSILO_INCLUDE_DIR=" + silo.prefix.include,
            "-DSILO_LIBRARY_DIR=" + silo.prefix.lib,
            "-DSILO_LIB=" + silo.libs.link_flags,
        ]
        return args
