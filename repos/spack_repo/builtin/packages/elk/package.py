# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class Elk(MakefilePackage):
    """An all-electron full-potential linearised augmented-plane wave
    (FP-LAPW) code with many advanced features."""

    homepage = "https://elk.sourceforge.io/"
    url = "https://sourceforge.net/projects/elk/files/elk-3.3.17.tgz"


    # what linear algebra packages to use? the choices are
    # internal - use internal libraries
    # generic  - use spack-provided blas and lapack
    # openblas - use openblas specifically, with special support for multithreading.
    # mkl - use mkl specifically, with special support for multithreading
    # should be used with fft=mkl
    # blis - use internal lapack and blas implementation from blis
    variant(
        "linalg",
        default="generic",
        multi=False,
        description="Build with custom BLAS library",
        values=("internal", "generic", "openblas", "mkl", "blis"),
    )
    # what FFT package to use? The choices are
    # internal - use internal library
    # fftw - fftw3 with special code
    # mkl  - use mklr with fft code
    # should be used with linalg=mkls
    variant(
        "fft",
        default="fftw",
        multi=False,
        description="Build with custom FFT library",
        values=("internal", "fftw", "mkl"),
    )
    #  check that if fft=mkl then linalg=mkl and vice versa.

    conflicts("linalg=mkl", when="fft=fftw")
    conflicts("linalg=mkl", when="fft=internal")
    conflicts("fft=mkl", when="linalg=internal")
    conflicts("fft=mkl", when="linalg=generic")
    conflicts("fft=mkl", when="linalg=openblas")
    conflicts("fft=mkl", when="linalg=blis")

    conflicts("linalg=internal", when="@8.6:", msg="Internal BLAS is not supported")
    conflicts("fft=internal", when="@8.6:", msg="Internal FFTW is not supported")
    conflicts("libxc@:6", when="@10:", msg="Versions >= 10 requires libxc >= 7")
    conflicts("libxc@7:", when="@:9", msg="Versions <=9 requires libxc =< 6")

    variant("mpi", default=True, description="Enable MPI parallelism")
    variant("openmp", default=True, description="Enable OpenMP support")
    variant("libxc", default=True, description="Link to Libxc functional library")
    variant("w90", default=False, description="wannier90 support, requires wannier90 library")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("blas", when="linalg=generic")
    depends_on("lapack", when="linalg=generic")

    depends_on("mkl", when="linalg=mkl")
    with when("linalg=mkl +openmp"):
        depends_on("intel-oneapi-mkl threads=openmp", when="^[virtuals=mkl] intel-oneapi-mkl")

    depends_on("openblas", when="linalg=openblas")
    depends_on("openblas threads=openmp", when="linalg=openblas +openmp")

    depends_on("blis", when="linalg=blis")
    depends_on("blis threads=openmp", when="linalg=blis +openmp")

    depends_on("fftw", when="fft=fftw")
    depends_on("fftw +openmp", when="fft=fftw +openmp")
    depends_on("mkl", when="fft=mkl")

    depends_on("mpi@2:", when="+mpi")
    depends_on("libxc@7:", when="@10:+libxc")
    depends_on("libxc@6:", when="@:9+libxc")
    depends_on("libxc@5:", when="@:7+libxc")
    depends_on("wannier90", when="+w90")

    # Cannot be built in parallel
    parallel = False

    def edit(self, spec, prefix):
        if spec.satisfies("@8.6:"):
            libxc_env_var_src = "SRC_LIBXC"
            libxc_env_var_lib = "LIB_LIBXC"
        else:
            libxc_env_var_src = "SRC_libxc"
            libxc_env_var_lib = "LIB_libxc"

        # Dictionary of configuration options with default values assigned
        config = {
            "MAKE": "make",
            "AR": "ar",
            "LIB_LPK": "lapack.a blas.a",
            "LIB_FFT": "fftlib.a",
            "SRC_MPI": "mpi_stub.f90",
            "SRC_MKL": "mkl_stub.f90",
            "SRC_OBLAS": "oblas_stub.f90",
            "SRC_OMP": "omp_stub.f90",
            "SRC_BLIS": "blis_stub.f90",
            libxc_env_var_src: "libxcifc_stub.f90",
            "SRC_FFT": "zfftifc.f90",
            "SRC_W90S": "w90_stub.f90",
            "F90": spack_fc,
            "F77": spack_f77,
        }
        # Compiler-specific flags

        flags = ""
        if self.compiler.name == "intel":
            flags = "-O3 -ip -unroll -no-prec-div"
        elif self.compiler.name == "gcc":
            flags = "-O3 -ffast-math -funroll-loops"
            if spec.satisfies("%gcc@10:"):
                flags += " -fallow-argument-mismatch "
        elif self.compiler.name == "g95":
            flags = "-O3 -fno-second-underscore"
        elif self.compiler.name == "nag":
            flags = "-O4 -kind=byte -dusty -dcfuns"
        elif self.compiler.name == "xl":
            flags = "-O3"
        config["F90_OPTS"] = flags
        config["F77_OPTS"] = flags

        if spec.satisfies("+mpi"):
            config["F90"] = spec["mpi"].mpifc
            config["F77"] = spec["mpi"].mpif77
            config["SRC_MPI"] = " "
        else:
            config["F90"] = spack_fc
            config["F77"] = spack_f77
            config["SRC_MPI"] = "mpi_stub.f90"

        # OpenMP support
        if spec.satisfies("+openmp"):
            config["F90_OPTS"] += " " + self.compiler.openmp_flag
            config["F77_OPTS"] += " " + self.compiler.openmp_flag
            config["SRC_OMP"] = " "

        # BLAS/LAPACK support
        # Note: openblas must be compiled with OpenMP support
        # if the +openmp variant is chosen
        if spec.satisfies("linalg=internal"):
            self.build_targets.append("blas")
            self.build_targets.append("lapack")
        if spec.satisfies("linalg=generic"):
            blas = spec["blas"].libs.joined()
            lapack = spec["lapack"].libs.joined()
            config["LIB_LPK"] = " ".join([lapack, blas])
        if spec.satisfies("linalg=openblas"):
            config["LIB_LPK"] = spec["openblas"].libs.ld_flags
            config["SRC_OBLAS"] = " "
        if spec.satisfies("linalg=mkl"):
            config["LIB_LPK"] = spec["mkl"].libs.ld_flags
            config["SRC_MKL"] = " "
        if spec.satisfies("linalg=blis"):
            config["LIB_LPK"] = " ".join(["lapack.a ", spec["blis"].libs.ld_flags])
            config["SRC_BLIS"] = " "
        # FFT
        if spec.satisfies("fft=internal"):
            self.build_targets.append("fft")
        elif spec.satisfies("fft=fftw"):
            config["LIB_FFT"] = spec["fftw"].libs.ld_flags
            config["SRC_FFT"] = "zfftifc_fftw.f90"
            if spec.satisfies("@8.6:"):
                config["LIB_FFT"] += " -lfftw3f"
                config["SRC_FFT"] += " cfftifc_fftw.f90"
        elif spec.satisfies("fft=mkl"):
            config["LIB_FFT"] = spec["mkl"].libs.ld_flags
            config["SRC_FFT"] = "mkl_dfti.f90 zfftifc_mkl.f90"
            if spec.satisfies("@8.6:"):
                config["SRC_FFT"] += " cfftifc_mkl.f90"
            cp = which("cp")
            mkl_prefix = spec["mkl"].prefix
            cp(
                join_path(mkl_prefix.include, "mkl_dfti.f90"),
                join_path(self.build_directory, "src"),
            )

        if spec.satisfies("@8.6:"):
            config["F90_LIB"] = " ".join([config["LIB_LPK"], config["LIB_FFT"]])
            del config["LIB_LPK"]
            del config["LIB_FFT"]

        # Define targets
        self.build_targets.append("elk")
        print(self.build_targets)
        # Libxc support
        if spec.satisfies("+libxc"):
            if self.spec.satisfies("@10:"):
                config[libxc_env_var_lib] = join_path(spec["libxc"].prefix.lib, "libxcf03.so")
            else:
                config[libxc_env_var_lib] = join_path(spec["libxc"].prefix.lib, "libxcf90.so")
            _libxc_lib = join_path(spec["libxc"].prefix.lib, "libxc.so")
            config[libxc_env_var_lib] += f" {_libxc_lib}"

            if self.spec.satisfies("@10:"):
                config[libxc_env_var_src] = "libxcf03.f90 libxcifc.f90"
            elif self.spec.satisfies("@7:9"):
                config[libxc_env_var_src] = "libxcf90.f90 libxcifc.f90"
            else:
                config[libxc_env_var_src] = "libxc_funcs.f90 libxc.f90 libxcifc.f90"

        # Write configuration options to include file
        with open("make.inc", "w") as inc:
            for key in config:
                inc.write("{0} = {1}\n".format(key, config[key]))

    def build(self, spec, prefix):
        with working_dir(self.build_directory + "/src"):
            make(*self.build_targets)
            make("-C", "eos")
            make("-C", "spacegroup")

    def install(self, spec, prefix):
        # The Elk Makefile does not provide an install target
        mkdir(prefix.bin)

        install("src/elk", prefix.bin)
        install("src/eos/eos", prefix.bin)
        install("src/spacegroup/spacegroup", prefix.bin)

        install_tree("examples", join_path(prefix, "examples"))
        install_tree("species", join_path(prefix, "species"))

    @on_package_attributes(run_tests=True)
    def check(self):
        with working_dir("{0}/tests".format(self.build_directory)):
            bash = which("bash")
            bash("./test.sh")
