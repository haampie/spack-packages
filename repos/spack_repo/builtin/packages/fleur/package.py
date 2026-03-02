# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.generic import Package

from spack.package import *


class Fleur(Package):
    """FLEUR (Full-potential Linearised augmented plane wave in EURope)
    is a code family for calculating groundstate as well as excited-state properties
    of solids within the context of density functional theory (DFT)."""

    homepage = "https://www.flapw.de/MaX-5.1"
    git = "https://iffgit.fz-juelich.de/fleur/fleur.git"

    license("MIT")

    version("develop", branch="develop")

    variant(
        "fft",
        default="internal",
        values=("internal", "mkl", "fftw"),
        description="Enable the use of Intel MKL FFT/FFTW provider",
    )
    variant("elpa", default=False, description="Enable ELPA support")
    variant("magma", default=False, description="Enable Magma support")
    variant("external_libxc", default=False, description="Enable external libxc support")
    variant("spfft", default=False, description="Enable spfft support")
    variant("wannier90", default=False, description="Enable wannier90 support")
    variant("openmp", default=False, description="Enable OpenMP support.")
    variant(
        "build_type",
        default="RelWithDebInfo",
        description="The build type to build",
        values=("Debug", "Release", "RelWithDebInfo"),
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("cmake", type="build")
    depends_on("python@3:", type="build")
    depends_on("blas")
    depends_on("lapack")
    depends_on("libxml2")
    depends_on("mpi", when="+mpi")
    depends_on("intel-oneapi-mkl", when="fft=mkl")
    depends_on("fftw-api", when="fft=fftw")
    depends_on("scalapack", when="+scalapack")
    depends_on("libxc", when="+external_libxc")
    depends_on("hdf5+hl+fortran", when="+hdf5")
    depends_on("magma+fortran", when="+magma")
    depends_on("wannier90", when="+wannier90")
    depends_on("gmake", type="build")

    conflicts("%intel@:16.0.4", msg="ifort version <16.0 will most probably not work correctly")
    conflicts("%gcc@:6.3.0", msg="gfortran is known to work with versions newer than v6.3")
    conflicts("~scalapack", when="+elpa", msg="ELPA requires scalapack support")
    conflicts("@:5.0", when="fft=fftw", msg="FFTW interface is supported from Fleur v5.0")

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        spec = self.spec

        if spec.satisfies("+mpi"):
            env.set("CC", spec["mpi"].mpicc, force=True)
            env.set("FC", spec["mpi"].mpifc, force=True)
            env.set("CXX", spec["mpi"].mpicxx, force=True)

    @run_before("install")
    def configure(self):
        spec = self.spec
        sh = which("bash")

        options = {
            "-link": [],
            "-libdir": [],
            "-includedir": [],
            # "-flags": []
        }

        options["-link"].append(spec["blas"].libs.link_flags)
        options["-libdir"].append(spec["blas"].prefix.lib)
        options["-includedir"].append(spec["blas"].prefix.include)

        options["-link"].append(spec["lapack"].libs.link_flags)
        options["-libdir"].append(spec["lapack"].prefix.lib)
        options["-includedir"].append(spec["lapack"].prefix.include)

        options["-link"].append(spec["libxml2"].libs.link_flags)
        options["-libdir"].append(spec["libxml2"].prefix.lib)
        options["-includedir"].append(spec["libxml2"].prefix.include)
        options["-includedir"].append(join_path(spec["libxml2"].prefix.include, "libxml2"))

        if spec.satisfies("fft=mkl"):
            options["-link"].append(spec["intel-oneapi-mkl"].libs.link_flags)
            options["-libdir"].append(spec["intel-oneapi-mkl"].prefix.lib)
            options["-includedir"].append(spec["intel-oneapi-mkl"].prefix.include)
        if spec.satisfies("fft=fftw"):
            options["-link"].append(spec["fftw-api"].libs.link_flags)
            options["-libdir"].append(spec["fftw-api"].prefix.lib)
            options["-includedir"].append(spec["fftw-api"].prefix.include)
        if spec.satisfies("+scalapack"):
            options["-link"].append(spec["scalapack"].libs.link_flags)
            options["-libdir"].append(spec["scalapack"].prefix.lib)
        if spec.satisfies("+external_libxc"):
            # Workaround: The fortran library is called libxcf90.a/so
            #    but spec['wannier90'].libs.link_flags return -lxc
            options["-link"].append("-lxcf90")
            options["-libdir"].append(spec["libxc"].prefix.lib)
            options["-includedir"].append(spec["libxc"].prefix.include)
        if spec.satisfies("+hdf5"):
            options["-link"].append(spec["hdf5"].libs.link_flags)
            options["-libdir"].append(spec["hdf5"].prefix.lib)
            options["-includedir"].append(spec["hdf5"].prefix.include)
        if spec.satisfies("+magma"):
            options["-link"].append(spec["magma"].libs.link_flags)
            options["-libdir"].append(spec["magma"].prefix.lib)
            options["-includedir"].append(spec["magma"].prefix.include)
        if spec.satisfies("+wannier90"):
            # Workaround: The library is not called wannier90.a/so
            #    for this reason spec['wannier90'].libs.link_flags fails!
            options["-link"].append("-lwannier")
            options["-libdir"].append(spec["wannier90"].prefix.lib)
        if spec.satisfies("+spfft"):
            options["-link"].append(spec["spfft"].libs.link_flags)
            # Workaround: The library is installed in /lib64 not /lib
            options["-libdir"].append(spec["spfft"].prefix.lib + "64")
            # Workaround: The library needs spfft.mod in include/spfft path
            options["-includedir"].append(join_path(spec["spfft"].prefix.include, "spfft"))
        if spec.satisfies("+elpa"):
            options["-link"].append(spec["elpa"].libs.link_flags)
            options["-libdir"].append(spec["elpa"].prefix.lib)
            # Workaround: The library needs elpa.mod in include/elpa_%VERS/modules
            options["-includedir"].append(spec["elpa"].prefix.include)
            options["-includedir"].append(spec["elpa"].headers.include_flags[2:])
            options["-includedir"].append(
                join_path(spec["elpa"].headers.include_flags[2:], "modules")
            )

        args = []
        args.append("-link")
        args.append(" ".join(options["-link"]))
        args.append("-libdir")
        args.append(" ".join(options["-libdir"]))
        args.append("-includedir")
        args.append(" ".join(options["-includedir"]))

        sh("configure.sh", *args)

    def install(self, spec, prefix):
        with working_dir("build"):
            make()
            mkdirp(prefix.bin)
            if spec.satisfies("+mpi"):
                install("fleur_MPI", prefix.bin)
            else:
                install("fleur", prefix.bin)
            install("inpgen", prefix.bin)
