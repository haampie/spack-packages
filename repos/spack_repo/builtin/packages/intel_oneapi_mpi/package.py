# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import re

from spack_repo.builtin.build_systems.oneapi import IntelOneApiLibraryPackage, IntelOneApiPackage

from spack.package import *


@IntelOneApiPackage.update_description
class IntelOneapiMpi(IntelOneApiLibraryPackage):
    """Intel MPI Library is a multifabric message-passing library that
    implements the open-source MPICH specification. Use the library
    to create, maintain, and test advanced, complex applications
    that perform better on high-performance computing (HPC)
    clusters based on Intel processors.

    """

    maintainers("rscohn2")

    homepage = "https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/mpi-library.html"

    version(
        "2021.14.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/1acd5e79-796c-401a-ab31-a3dc7b20c6a2/intel-mpi-2021.14.1.7_offline.sh",
        sha256="6459b9fc81fad9b9955de7fd9904e67fcf2ada3564ce0a74b9c14ea8fb533ddf",
        expand=False,
    )
    version(
        "2021.14.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/4b14b28c-2ca6-4559-a0ca-8a157627e0c8/intel-mpi-2021.14.0.791_offline.sh",
        sha256="81ea7aaf8039c134b4df40bab1423a269425d26bb90ac05f7decac39719d21f3",
        expand=False,
    )
    version(
        "2021.13.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/364c798c-4cad-4c01-82b5-e1edd1b476af/l_mpi_oneapi_p_2021.13.1.769_offline.sh",
        sha256="be61c4792d25bd4a1b5f7b808c06a9f4676f1b247d7605ac6d3c6cffdb8f19b7",
        expand=False,
    )
    version(
        "2021.10.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/4f5871da-0533-4f62-b563-905edfb2e9b7/l_mpi_oneapi_p_2021.10.0.49374_offline.sh",
        sha256="ab2e97d87b139201a2e7dab9a61ac6e8927b7783b459358c4ad69a1b1c064f40",
        expand=False,
    )
    version(
        "2021.9.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/718d6f8f-2546-4b36-b97b-bc58d5482ebf/l_mpi_oneapi_p_2021.9.0.43482_offline.sh",
        sha256="5c170cdf26901311408809ced28498b630a494428703685203ceef6e62735ef8",
        expand=False,
    )
    version(
        "2021.8.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/19131/l_mpi_oneapi_p_2021.8.0.25329_offline.sh",
        sha256="0fcb1171fc42fd4b2d863ae474c0b0f656b0fa1fdc1df435aa851ccd6d1eaaf7",
        expand=False,
    )
    version(
        "2021.7.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/19010/l_mpi_oneapi_p_2021.7.1.16815_offline.sh",
        sha256="90e7804f2367d457cd4cbf7aa29f1c5676287aa9b34f93e7c9a19e4b8583fff7",
        expand=False,
    )
    version(
        "2021.4.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18186/l_mpi_oneapi_p_2021.4.0.441_offline.sh",
        sha256="cc4b7072c61d0bd02b1c431b22d2ea3b84b967b59d2e587e77a9e7b2c24f2a29",
        expand=False,
    )
    version(
        "2021.3.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/17947/l_mpi_oneapi_p_2021.3.0.294_offline.sh",
        sha256="04c48f864ee4c723b1b4ca62f2bea8c04d5d7e3de19171fd62b17868bc79bc36",
        expand=False,
    )
    version(
        "2021.2.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/17729/l_mpi_oneapi_p_2021.2.0.215_offline.sh",
        sha256="d0d4cdd11edaff2e7285e38f537defccff38e37a3067c02f4af43a3629ad4aa3",
        expand=False,
    )
    version(
        "2021.1.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/17397/l_mpi_oneapi_p_2021.1.1.76_offline.sh",
        sha256="8b7693a156c6fc6269637bef586a8fd3ea6610cac2aae4e7f48c1fbb601625fe",
        expand=False,
    )

    variant("ilp64", default=False, description="Build with ILP64 support")
    variant(
        "generic-names",
        default=False,
        description="Use generic names, e.g mpicc instead of mpiicx",
    )
    variant(
        "classic-names",
        default=False,
        description="Use classic compiler names, e.g mpiicc instead of mpiicx",
    )
    variant(
        "external-libfabric", default=False, description="Enable external libfabric dependency"
    )
    depends_on("libfabric", when="+external-libfabric", type=("link", "run"))

    provides("mpi@:3.1")
    conflicts("+generic-names +classic-names")

    executables = [r"^mpiicpx$"]

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("-v", output=str, error=str)
        match = re.search(r"MPI Library (20\d\d(\.\d+)+)", output)
        return match.group(1) if match else None

    @classmethod
    def determine_variants(cls, exes, version_str):
        output = Executable(exes[0])("-show", output=str, error=str)
        lib_paths = re.findall(r'-L"?([^\s"]+)"?', output)
        variants_set = set()
        for lib_path in set(lib_paths):
            mpi_root = join_path(lib_path, "..")
            # Look for ilp64
            if os.path.exists(join_path(lib_path, "libmpi_ilp64.so")):
                variants_set.add("+ilp64")
            # Look for libfabric
            libfabric_dir = join_path(mpi_root, "opt/mpi/libfabric/lib")
            if os.path.exists(join_path(libfabric_dir, "libfabric.so")):
                variants_set.add("~external-libfabric")
            # If generic executables don't exist, disable the variant
            mpicxx_path = join_path(mpi_root, "bin", "mpicxx")
            if not os.path.exists(mpicxx_path):
                variants_set.add("~generic-names")
            # If classic executables don't exist, disable the variant
            mpiicpc_path = join_path(mpi_root, "bin", "mpiicpc")
            if not os.path.exists(mpiicpc_path):
                variants_set.add("~classic-names")

        if "+ilp64" not in variants_set:
            variants_set.add("~ilp64")
        if "~external-libfabric" not in variants_set:
            variants_set.add("+external-libfabric")

        return "".join(list(variants_set))

    @property
    def mpiexec(self):
        return self.component_prefix.bin.mpiexec

    @property
    def v2_layout_versions(self):
        return "@2021.11:"

    @property
    def component_dir(self):
        return "mpi"

    @property
    def env_script_args(self):
        if self.spec.satisfies("+external-libfabric"):
            return ("-i_mpi_ofi_internal=0",)
        else:
            return ()

    def wrapper_names(self):
        if self.spec.satisfies("+generic-names"):
            return ["mpicc", "mpicxx", "mpif77", "mpif90", "mpifc"]
        elif self.spec.satisfies("+classic-names"):
            return ["mpiicc", "mpiicpc", "mpiifort", "mpiifort", "mpiifort"]
        else:
            return ["mpiicx", "mpiicpx", "mpiifx", "mpiifx", "mpiifx"]

    def wrapper_paths(self):
        return [self.component_prefix.bin.join(name) for name in self.wrapper_names()]

    def setup_dependent_package(self, module, dep_spec):
        wrappers = self.wrapper_paths()
        self.spec.mpicc = wrappers[0]
        self.spec.mpicxx = wrappers[1]
        self.spec.mpif77 = wrappers[2]
        # no self.spec.mpif90
        self.spec.mpifc = wrappers[4]

    def setup_dependent_build_environment(
        self, env: EnvironmentModifications, dependent_spec: Spec
    ) -> None:
        dependent_module = dependent_spec.package.module
        for var_name, attr_name in (
            ("I_MPI_CC", "spack_cc"),
            ("I_MPI_CXX", "spack_cxx"),
            ("I_MPI_FC", "spack_fc"),
            ("I_MPI_F90", "spack_fc"),
            ("I_MPI_F77", "spack_f77"),
        ):
            if hasattr(dependent_module, attr_name):
                env.set(var_name, getattr(dependent_module, attr_name))

        # Set compiler wrappers for dependent build stage
        wrappers = self.wrapper_paths()
        env.set("MPICC", wrappers[0])
        env.set("MPICXX", wrappers[1])
        env.set("MPIF77", wrappers[2])
        env.set("MPIF90", wrappers[3])
        env.set("MPIFC", wrappers[4])

        env.set("I_MPI_ROOT", self.component_prefix)

    @property
    def libs(self):
        libs = []
        if self.spec.satisfies("+ilp64"):
            libs += find_libraries("libmpi_ilp64", self.component_prefix.lib.release)
        libs += find_libraries(["libmpicxx", "libmpifort"], self.component_prefix.lib)
        libs += find_libraries("libmpi", self.component_prefix.lib.release)
        libs += find_system_libraries(["libdl", "librt", "libpthread"])

        # Find libfabric for libmpi.so
        if self.spec.satisfies("+external-libfabric"):
            libs += self.spec["libfabric"].libs
        else:
            libs += find_libraries(["libfabric"], self.component_prefix.libfabric.lib)

        return libs

    @run_after("install")
    def fix_wrappers(self):
        # When spack builds from source
        # fix I_MPI_SUBSTITUTE_INSTALLDIR and
        #   __EXEC_PREFIX_TO_BE_FILLED_AT_INSTALL_TIME__
        for wrapper in ["mpif77", "mpif90", "mpigcc", "mpigxx", "mpiicc", "mpiicpc", "mpiifort"]:
            filter_file(
                r"I_MPI_SUBSTITUTE_INSTALLDIR|" r"__EXEC_PREFIX_TO_BE_FILLED_AT_INSTALL_TIME__",
                self.component_prefix,
                self.component_prefix.bin.join(wrapper),
                backup=False,
            )

    @run_after("install")
    def fixup_prefix(self):
        # The motivation was to provide a more standard layout so impi
        # would be more likely to work as a virtual dependence.  It
        # does not work for v2_layout because of a library conflict. I
        # am not sure if this mechanism is useful so disabling for
        # v2_layout rather than try to make it work.
        if self.v2_layout:
            return
        self.symlink_dir(self.component_prefix.include, self.prefix.include)
        self.symlink_dir(self.component_prefix.lib, self.prefix.lib)
        self.symlink_dir(self.component_prefix.lib.release, self.prefix.lib)
        self.symlink_dir(self.component_prefix.bin, self.prefix.bin)
