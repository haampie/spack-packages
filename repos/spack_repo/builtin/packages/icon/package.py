# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from collections import defaultdict

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.cuda import CudaPackage

from spack.package import *


class Icon(AutotoolsPackage):
    """ICON - is a modeling framework for weather, climate, and environmental prediction. It solves
    the full three-dimensional non-hydrostatic and compressible Navier-Stokes equations on an
    icosahedral grid and allows seamless predictions from local to global scales."""

    homepage = "https://www.icon-model.org"
    url = "https://gitlab.dkrz.de/icon/icon-model/-/archive/icon-2024.01-public/icon-model-icon-2024.01-public.tar.gz"
    git = "https://gitlab.dkrz.de/icon/icon-model.git"
    submodules = True

    maintainers("skosukhin", "Try2Code")

    license("BSD-3-Clause", checked_by="skosukhin")

    version(
        "2025.04", tag="icon-2025.04-public", commit="1be2ca66ea0de149971d2e77e88a9f11c764bd22"
    )
    version("2024.10", sha256="5c461c783eb577c97accd632b18140c3da91c1853d836ca2385f376532e9bad1")
    version("2024.07", sha256="f53043ba1b36b8c19d0d2617ab601c3b9138b90f8ff8ca6db0fd079665eb5efa")
    version("2024.01-1", sha256="3e57608b7e1e3cf2f4cb318cfe2fdb39678bd53ca093955d99570bd6d7544184")
    version("2024.01", sha256="d9408fdd6a9ebf5990298e9a09c826e8c15b1e79b45be228f7a5670a3091a613")

    # Model Features:
    variant("atmo", default=True, description="Enable the atmosphere component")
    variant("les", default=True, description="Enable the Large-Eddy Simulation component")
    variant("upatmo", default=True, description="Enable the upper atmosphere component")
    variant("ocean", default=True, description="Enable the ocean component")
    variant("jsbach", default=True, description="Enable the land component JSBACH")
    variant("waves", default=True, description="Enable the ocean surface wave component")
    variant("coupling", default=True, description="Enable the coupling")
    variant("aes", default=True, description="Enable the AES physics package")
    variant("nwp", default=True, description="Enable the NWP physics package")
    variant(
        "ecrad", default=False, description="Enable usage of the ECMWF radiation scheme (ECRAD)"
    )
    variant(
        "rte-rrtmgp",
        default=True,
        description="Enable usage of the RTE+RRTMGP toolbox for radiation calculations",
    )
    variant(
        "art", default=False, description="Enable the aerosols and reactive trace component ART"
    )

    # Infrastructural Features:
    variant("mpi", default=True, description="Enable MPI (parallelization) support")
    variant("openmp", default=False, description="Enable OpenMP support")

    nvidia_targets = {"nvidia-{0}".format(cc): cc for cc in CudaPackage.cuda_arch_values}
    # TODO: add AMD GPU support

    variant(
        "gpu",
        default="none",
        values=("none",) + tuple(nvidia_targets.keys()),
        description="Enable GPU support for the specified architecture",
    )
    for __x in nvidia_targets.keys():
        # Other compilers are not yet tested or supported, older NVHPC versions are not supported:
        requires("%nvhpc@21.3:", when="gpu={0}".format(__x))

    variant("mpi-gpu", default=True, description="Enable usage of the GPU-aware MPI features")
    requires("+mpi", when="+mpi-gpu")
    conflicts("gpu=none", when="+mpi-gpu")

    variant("grib2", default=False, description="Enable GRIB2 I/O")

    variant(
        "parallel-netcdf",
        default=False,
        description="Enable usage of the parallel features of NetCDF",
    )
    requires("+mpi", when="+parallel-netcdf")

    variant("cdi-pio", default=False, description="Enable usage of the parallel features of CDI")
    requires("+mpi", when="+cdi-pio")

    variant("yaxt", default=False, description="Enable the YAXT data exchange")

    serialization_values = ("read", "perturb", "create")


    # Optimization Features:
    variant("mixed-precision", default=False, description="Enable mixed-precision dynamical core")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build")
    depends_on("python", type="build")

    depends_on("libxml2", when="+art")
    depends_on("libfyaml@0.6:", when="+coupling")
    for __x in serialization_values:
        depends_on("serialbox+fortran", when="serialization={0}".format(__x))
    depends_on("eccodes", when="+grib2")
    depends_on("lapack")
    depends_on("blas")
    depends_on("netcdf-fortran")
    depends_on("netcdf-c")
    depends_on("netcdf-c+mpi", when="+parallel-netcdf")
    depends_on("mpi", when="+mpi")

    for __x in nvidia_targets.keys():
        depends_on("cuda", when="gpu={0}".format(__x))

