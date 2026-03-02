# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Adios(AutotoolsPackage):
    """The Adaptable IO System (ADIOS) provides a simple,
    flexible way for scientists to describe the
    data in their code that may need to be written,
    read, or processed outside of the running simulation.
    """

    homepage = "https://www.olcf.ornl.gov/center-projects/adios/"
    url = "https://github.com/ornladios/ADIOS/archive/v1.12.0.tar.gz"
    git = "https://github.com/ornladios/ADIOS.git"


    version("1.13.0", sha256="7b5ee8ff7a5f7215f157c484b20adb277ec0250f87510513edcc25d2c4739f50")
    version("1.9.0", sha256="23b2bb70540d51ab0855af0b205ca484fd1bd963c39580c29e3133f9e6fffd46")

    variant("shared", default=True, description="Builds a shared version of the library")

    variant("fortran", default=False, description="Enable Fortran bindings support")

    variant("mpi", default=True, description="Enable MPI support")
    variant("infiniband", default=False, description="Enable infiniband support")

    # transforms
    variant("zlib", default=True, description="Enable zlib transform support")
    variant("bzip2", default=False, description="Enable bzip2 transform support")
    variant("szip", default=False, description="Enable szip transform support")
    variant("zfp", default=True, description="Enable ZFP transform support")
    variant("sz", default=True, description="Enable SZ transform support")
    variant("lz4", default=True, description="Enable LZ4 transform support")
    variant("blosc", default=True, description="Enable Blosc transform support")
    # transports and serial file converters
    variant(
        "hdf5",
        default=False,
        description="Enable parallel HDF5 transport and serial bp2h5 " + "converter",
    )
    variant("netcdf", default=False, description="Enable netcdf support")

    variant(
        "staging",
        values=any_combination_of("flexpath", "dataspaces"),
        description="Enable dataspaces and/or flexpath staging transports",
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated


    # optional transformations
    depends_on("zlib-api", when="+zlib")
    depends_on("bzip2", when="+bzip2")
    depends_on("szip", when="+szip")
    depends_on("sz@:1.4.10", when="@:1.12.0 +sz")
    depends_on("sz@1.4.11.0:1.4.11", when="@1.13.0 +sz")
    depends_on("lz4", when="+lz4")
    # optional transports & file converters
    depends_on("dataspaces+mpi", when="staging=dataspaces")

    for p in ["+hdf5", "+netcdf", "staging=flexpath", "staging=dataspaces"]:
        conflicts(p, when="~mpi")

    build_directory = "spack-build"

    # ADIOS uses the absolute Python path, which is too long and results in
    # "bad interpreter" errors - but not applicable for 1.9.0
    # Fix ADIOS <=1.10.0 compile error on HDF5 1.10+
    #   https://github.com/ornladios/ADIOS/commit/3b21a8a41509
    #   https://github.com/spack/spack/issues/1683

    # ADIOS 1.13.1 is written for ZFP 0.5.0 interfaces
    #   https://github.com/ornladios/ADIOS/pull/204

    # Fix a bug in configure.ac that causes automake issues on RHEL 7.7

    def with_or_without_hdf5(self, activated):
        if activated:
            return f"--with-phdf5={self.spec['hdf5'].prefix}"

        return "--without-phdf5"

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        # https://github.com/ornladios/ADIOS/issues/206
        if self.spec.satisfies("+fortran %gcc@10:"):
            env.set("FCFLAGS", "-fallow-argument-mismatch")

    def configure_args(self):
        spec = self.spec

        extra_args = [
            # required, otherwise building its python bindings will fail
            f"CFLAGS={self.compiler.cc_pic_flag}"
        ]

        extra_args += self.enable_or_disable("shared")
        extra_args += self.enable_or_disable("fortran")

        if spec.satisfies("+mpi"):
            env["MPICC"] = spec["mpi"].mpicc
            env["MPICXX"] = spec["mpi"].mpicxx

        extra_args += self.with_or_without("mpi", activation_value="prefix")
        extra_args += self.with_or_without("infiniband")

        if spec.satisfies("+zlib"):
            extra_args.append(f"--with-zlib={spec['zlib-api'].prefix}")
        else:
            extra_args.append("--without-zlib")

        # Transforms
        variants = ["bzip2", "szip"]
        if spec.satisfies("@1.11.0:"):
            variants += ["zfp"]
        if spec.satisfies("@1.12.0:"):
            variants += ["sz", "lz4"]
        if spec.satisfies("@1.13.0:"):
            extra_args += self.with_or_without(
                "blosc", activation_value=lambda x: spec["c-blosc"].prefix
            )

        # External I/O libraries
        variants += ["hdf5", "netcdf"]

        for x in variants:
            extra_args += self.with_or_without(x, activation_value="prefix")

        # Staging transports
        def with_staging(name):
            if name == "flexpath":
                return spec["libevpath"].prefix
            return spec[name].prefix

        extra_args += self.with_or_without("staging", activation_value=with_staging)

        return extra_args
