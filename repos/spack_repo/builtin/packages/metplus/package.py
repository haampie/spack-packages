# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.generic import Package

from spack.package import *


class Metplus(Package):
    """
    METplus is a verification framework that spans a wide range of temporal
    (warn-on-forecast to climate) and spatial (storm to global) scales.
    """

    homepage = "https://dtcenter.org/community-code/metplus"
    url = "https://github.com/dtcenter/METplus/archive/refs/tags/v4.1.0.tar.gz"
    git = "https://github.com/dtcenter/METplus"



    variant("tcmpr_plotter", default=False, description="Enable TCMPRPlotter.")
    variant("series_analysis", default=False, description="Enable CyclonePlotter wrapper.")
    variant("cycloneplotter", default=False, description="Enable CyclonePlotter wrapper.")
    variant("makeplots", default=False, description="Enable MakePlots Wrapper.")
    variant("plotdataplane", default=False, description="Generate images from Postscript output.")

    depends_on("python@3.10.4:", when="@6:", type=("run"))
    depends_on("met+python", type=("run"))
    depends_on("met@12:+python", when="@6:", type=("run"))
    # https://metplus.readthedocs.io/en/main_v6.0/Users_Guide/installation.html
    depends_on("netcdf-c")
    depends_on("netcdf-c@1.5.4:", when="@6:")
    depends_on("py-python-dateutil", type=("run"))
    depends_on("py-python-dateutil@2.8:", when="@6:", type=("run"))
    depends_on("py-python-dateutil@2.8.2:", when="@6.1:", type=("run"))

    depends_on("py-cartopy", when="+makeplots", type=("run"))
    depends_on("py-cartopy@0.20.3:", when="@6: +makeplots", type=("run"))
    depends_on("py-matplotlib", when="+cycloneplotter", type=("run"))
    depends_on("py-matplotlib@3.5.2", when="@6: +cycloneplotter", type=("run"))
    depends_on("py-cartopy", when="+cycloneplotter", type=("run"))

    depends_on("r", when="+tcmpr_plotter", type=("run"))
    depends_on("imagemagick", when="+series_analysis", type=("run"))
    depends_on("imagemagick", when="+plotdataplane", type=("run"))

    def install(self, spec, prefix):
        if spec.satisfies("@4.0.0:"):
            conf = "defaults.conf"
        else:
            conf = "metplus_system.conf"

        metplus_config = FileFilter(join_path("parm", "metplus_config", conf))

        met_prefix = spec["met"].prefix
        metplus_config.filter(
            r"MET_INSTALL_DIR = /path/to", "MET_INSTALL_DIR = {}".format(met_prefix)
        )

        install_tree(self.stage.source_path, prefix)

    def setup_run_environment(self, env: EnvironmentModifications) -> None:
        env.prepend_path("PATH", self.prefix.ush)
