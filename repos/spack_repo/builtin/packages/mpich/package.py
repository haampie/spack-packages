# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import sys

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.rocm import ROCmPackage

from spack.package import *


class MpichEnvironmentModifications(PackageBase):
    """Collects the environment modifications that are usually needed for the life-cycle of
    MPICH, and derivatives.
    """

class Mpich(MpichEnvironmentModifications, AutotoolsPackage, CudaPackage, ROCmPackage):
    """MPICH is a high performance and widely portable implementation of
    the Message Passing Interface (MPI) standard."""

    homepage = "https://www.mpich.org"
    url = "https://www.mpich.org/static/downloads/3.0.4/mpich-3.0.4.tar.gz"
    git = "https://github.com/pmodels/mpich.git"
    list_url = "https://www.mpich.org/static/downloads/"
    list_depth = 1

    tags = ["e4s"]
    executables = ["^mpichversion$"]

    keep_werror = "specific"

    version("4.2.1", sha256="23331b2299f287c3419727edc2df8922d7e7abbb9fd0ac74e03b9966f9ad42d7")
    version("4.2.0", sha256="a64a66781b9e5312ad052d32689e23252f745b27ee8818ac2ac0c8209bc0b90e")
    version("4.1.2", sha256="3492e98adab62b597ef0d292fb2459b6123bc80070a8aa0a30be6962075a12f0")
    version("4.1.1", sha256="ee30471b35ef87f4c88f871a5e2ad3811cd9c4df32fd4f138443072ff4284ca2")
    version("4.1", sha256="8b1ec63bc44c7caa2afbb457bc5b3cd4a70dbe46baba700123d67c48dc5ab6a0")
    version("4.0.3", sha256="17406ea90a6ed4ecd5be39c9ddcbfac9343e6ab4f77ac4e8c5ebe4a3e3b6c501")
    version("4.0.2", sha256="5a42f1a889d4a2d996c26e48cbf9c595cbf4316c6814f7c181e3320d21dedd42")
    version("4.0.1", sha256="66a1fe8052734af2eb52f47808c4dfef4010ceac461cb93c42b99acfb1a43687")
    version("4.0", sha256="df7419c96e2a943959f7ff4dc87e606844e736e30135716971aba58524fbff64")
    version("3.4.3", sha256="8154d89f3051903181018166678018155f4c2b6f04a9bb6fe9515656452c4fd7")
    version("3.4.2", sha256="5c19bea8b84e8d74cca5f047e82b147ff3fba096144270e3911ad623d6c587bf")
    version("3.4.1", sha256="8836939804ef6d492bcee7d54abafd6477d2beca247157d92688654d13779727")
    version("3.4", sha256="ce5e238f0c3c13ab94a64936060cff9964225e3af99df1ea11b130f20036c24b")
    version("3.3.2", sha256="4bfaf8837a54771d3e4922c84071ef80ffebddbb6971a006038d91ee7ef959b9")
    version("3.3.1", sha256="fe551ef29c8eea8978f679484441ed8bb1d943f6ad25b63c235d4b9243d551e5")
    version("3.3", sha256="329ee02fe6c3d101b6b30a7b6fb97ddf6e82b28844306771fa9dd8845108fa0b")
    version("3.2.1", sha256="5db53bf2edfaa2238eb6a0a5bc3d2c2ccbfbb1badd79b664a1a919d2ce2330f1")
    version("3.2", sha256="0778679a6b693d7b7caff37ff9d2856dc2bfc51318bf8373859bfa74253da3dc")
    version("3.1.4", sha256="f68b5330e94306c00ca5a1c0e8e275c7f53517d01d6c524d51ce9359d240466b")
    version("3.1.3", sha256="afb690aa828467721e9d9ab233fe00c68cae2b7b930d744cb5f7f3eb08c8602c")
    version("3.1.2", sha256="37c3ba2d3cd3f4ea239497d9d34bd57a663a34e2ea25099c2cbef118c9156587")
    version("3.1.1", sha256="455ccfaf4ec724d2cf5d8bff1f3d26a958ad196121e7ea26504fd3018757652d")
    version("3.1", sha256="fcf96dbddb504a64d33833dc455be3dda1e71c7b3df411dfcf9df066d7c32c39")
    version("3.0.4", sha256="cf638c85660300af48b6f776e5ecd35b5378d5905ec5d34c3da7a27da0acf0b3")

    variant("hwloc", default=True, description="Use external hwloc package")
    variant("hydra", default=True, description="Build the hydra process manager")
    variant("romio", default=True, description="Enable ROMIO MPI I/O implementation")
    variant("verbs", default=False, description="Build support for OpenFabrics verbs.")
    variant("slurm", default=False, description="Enable Slurm support")
    variant("wrapperrpath", default=True, description="Enable wrapper rpath")
    variant(
        "pmi",
        default="default",
        description="""PMI interface.""",
        values=("default", "pmi", "pmi2", "pmix", "cray"),
        multi=False,
    )
    variant(
        "device",
        default="ch4",
        description="""Abstract Device Interface (ADI)
implementation. The ch4 device is in experimental state for versions
before 3.4.""",
        values=("ch3", "ch4", "ch3:sock"),
        multi=False,
    )
    variant(
        "netmod",
        default="ofi",
        description="""Network module. Only single netmod builds are
supported, and netmod is ignored if device is ch3:sock.""",
        values=("tcp", "mxm", "ofi", "ucx"),
        multi=False,
    )
    variant(
        "pci",
        default=(sys.platform != "darwin"),
        description="Support analyzing devices on PCI bus",
    )
    variant(
        "libxml2",
        default=True,
        description="Use libxml2 for XML support instead of the custom "
        "minimalistic implementation",
    )
    variant("argobots", default=False, description="Enable Argobots support")
    variant("fortran", default=True, description="Enable Fortran support")

    variant(
        "vci",
        default=False,
        when="@4: device=ch4",
        description="Enable multiple VCI (virtual communication "
        "interface) critical sections to improve performance "
        "of applications that do heavy concurrent MPI"
        "communications. Set MPIR_CVAR_CH4_NUM_VCIS=<N> to "
        "enable multiple vcis at runtime.",
    )

    variant(
        "datatype-engine",
        default="auto",
        description="controls the datatype engine to use",
        values=("dataloop", "yaksa", "auto"),
        when="@3.4:",
        multi=False,
    )
    for _yaksa_cond in (
        "@4.0:4.3 device=ch4 datatype-engine=auto",
        "@4.0:4.3 device=ch4 datatype-engine=yaksa",
    ):
        with when(_yaksa_cond):
            depends_on("yaksa")
            depends_on("yaksa+cuda", when="+cuda")
            depends_on("yaksa+rocm", when="+rocm")

    variant(
        "hcoll",
        default=False,
        description="Enable support for Mellanox HCOLL accelerated collective operations library",
        when="@3.3: device=ch4 netmod=ucx",
    )

    variant("xpmem", default=False, when="@3.4:", description="Enable XPMEM support")
    variant("level_zero", default=False, description="Enable level zero support")

    conflicts("datatype-engine=yaksa", when="device=ch3")
    conflicts("datatype-engine=yaksa", when="device=ch3:sock")
    conflicts("datatype-engine=dataloop", when="+cuda")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build", when="+fortran")

    depends_on("hcoll", when="+hcoll")
    depends_on("xpmem", when="+xpmem")

    # Todo: cuda can be a conditional variant, but it does not seem to work when
    # overriding the variant from CudaPackage.

    provides("mpi@:4.0")
    provides("mpi@:3.1", when="@:3.2")
    provides("mpi@:3.0", when="@:3.1")
    provides("mpi@:2.2", when="@:1.2")
    provides("mpi@:2.1", when="@:1.1")
    provides("mpi@:2.0", when="@:1.0")

    filter_compiler_wrappers("mpicc", "mpicxx", "mpif77", "mpif90", "mpifort", relative_root="bin")
    # Set correct rpath flags for Intel Fortran Compiler (%oneapi)
    # See https://github.com/pmodels/mpich/pull/5824
    # and https://github.com/spack/spack/issues/31678
    # We do not fetch the patch from the upstream repo because it cannot be applied to older
    # versions.
    with when("%oneapi"):
        patch("mpich-oneapi-config-rpath/step1.patch", when="@:4.0.2")
        patch("mpich-oneapi-config-rpath/step2.patch", when="@3.1.1:4.0.2")

    # Fix using an external hwloc
    # See https://github.com/pmodels/mpich/issues/4038
    # and https://github.com/pmodels/mpich/pull/3540
    # landed in v3.4b1 v3.4a3
    patch(
        "https://github.com/pmodels/mpich/commit/8a851b317ee57366cd15f4f28842063d8eff4483.patch?full_index=1",
        sha256="d2dafc020941d2d8cab82bc1047e4a6a6d97736b62b06e2831d536de1ac01fd0",
        when="@3.3 +hwloc",
    )

    # fix MPI_Barrier segmentation fault
    # see https://lists.mpich.org/pipermail/discuss/2016-May/004764.html
    # and https://lists.mpich.org/pipermail/discuss/2016-June/004768.html
    patch("mpich32_clang.patch", when="@=3.2%clang")
    patch("mpich32_clang.patch", when="@=3.2%apple-clang")

    # Fix SLURM node list parsing
    # See https://github.com/pmodels/mpich/issues/3572
    # and https://github.com/pmodels/mpich/pull/3578
    patch(
        "https://github.com/pmodels/mpich/commit/b324d2de860a7a2848dc38aefb8c7627a72d2003.patch?full_index=1",
        sha256="5f48d2dd8cc9f681cf710b864f0d9b00c599f573a75b1e1391de0a3d697eba2d",
        when="@=3.3",
    )

    # Fix SLURM hostlist_t usage
    # See https://github.com/pmodels/mpich/issues/6806
    # and https://github.com/pmodels/mpich/pull/6820
    patch(
        "https://github.com/pmodels/mpich/commit/7a28682a805acfe84a4ea7b41cea079696407398.patch?full_index=1",
        sha256="8cc80a8ffc3f1c907b1d8176129a0c1d01794a95adbed5b5357f50c13f6560e4",
        when="@4.1:4.1.2 +slurm ^slurm@23-11-1-1:",
    )
    # backports of fix down to v3.3
    patch(
        "mpich40_slurm_hostlist.patch",
        sha256="39aa1353305b7b03bc5c645c87d5299bd5d2ff676750898ba925f6cb9b716bdb",
        when="@4.0 +slurm ^slurm@23-11-1-1:",
    )
    patch(
        "mpich33_slurm_hostlist.patch",
        sha256="d6ec26adcf2d08d0739be44ab65b928a7a88e9ff1375138a0593678eedd420ab",
        when="@3.3:3.4 +slurm ^slurm@23-11-1-1:",
    )

    # Fix reduce operations for unsigned integers
    # See https://github.com/pmodels/mpich/issues/6083
    patch(
        "https://github.com/pmodels/mpich/commit/3a1f618e017547c9710ab4fb01ae258a01477190.patch?full_index=1",
        sha256="d4c0e99a80f6cb0cb0ced91f6ad5da776c4a70f70f805f08096939ec9a92483e",
        when="@4.0:4.0.2",
    )

    # Fix checking whether the datatype is contiguous
    # https://github.com/pmodels/yaksa/pull/189
    # https://github.com/pmodels/mpich/issues/5391
    # The problem has been fixed starting version 4.0 by updating the yaksa git submodule, which
    # has not been done for the 3.4.x branch. The following patch is a backport of the
    # aforementioned pull request for the unreleased version of yaksa that is vendored with MPICH.
    # Note that Spack builds MPICH against a non-vendored yaksa only starting version 4.0.
    with when("@3.4"):
        # Apply the patch only when yaksa is used:
        patch("mpich34_yaksa_hindexed.patch", when="datatype-engine=yaksa")
        patch("mpich34_yaksa_hindexed.patch", when="datatype-engine=auto device=ch4")

    # Fix false positive result of the configure time check for CFI support
    # https://github.com/pmodels/mpich/pull/6537
    # https://github.com/pmodels/mpich/issues/6505
    with when("@3.2.2:4.1.1"):
        # Apply the patch from the upstream repo in case we have to run the autoreconf stage:
        patch(
            "https://github.com/pmodels/mpich/commit/d901a0b731035297dd6598888c49322e2a05a4e0.patch?full_index=1",
            sha256="de0de41ec42ac5f259ea02f195eea56fba84d72b0b649a44c947eab6632995ab",
        )
        # Apply the changes to the configure script to skip the autoreconf stage if possible:
        patch("mpich32_411_CFI_configure.patch")

    depends_on("findutils", type="build")
    depends_on("pkgconfig", type="build")

    depends_on("hwloc@2.0.0:", when="@3.3: +hwloc")
    depends_on("hwloc@2.0.0: +cuda", when="@3.3: +cuda+hwloc")

    depends_on("libfabric", when="netmod=ofi")
    depends_on("libfabric+cuda", when="+cuda netmod=ofi")
    # The ch3 ofi netmod results in crashes with libfabric 1.7
    # See https://github.com/pmodels/mpich/issues/3665
    depends_on("libfabric@:1.6", when="device=ch3 netmod=ofi")
    depends_on("libfabric@1.5:", when="@3.4: device=ch4 netmod=ofi")

    depends_on("ucx", when="netmod=ucx")
    depends_on("ucx+cuda", when="+cuda netmod=ucx")
    depends_on("mxm", when="netmod=mxm")

    # The dependencies on libpciaccess and libxml2 come from the embedded
    # hwloc, which, before version 3.3, was used only for Hydra.
    depends_on("libpciaccess", when="@:3.2+hydra+pci")
    depends_on("libxml2", when="@:3.2+hydra+libxml2")

    # Starting with version 3.3, MPICH uses hwloc directly.

    # Starting with version 3.3, Hydra can use libslurm for nodelist parsing


    # +argobots variant requires Argobots

    # building from git requires regenerating autotools files

    # building with "+hwloc' also requires regenerating autotools files

    # MPICH's Yaksa submodule requires python to configure



    # MPICH does not require libxml2 and libpciaccess for versions before 3.3
    # when ~hydra is set: prevent users from setting +libxml2 and +pci in this
    # case to avoid generating an identical MPICH installation.

    # see https://github.com/pmodels/mpich/pull/5031

    def test_sendrecv(self):
        """build and run sendrecv"""
        self.run_mpich_test(join_path("test", "mpi", "basic"), "sendrecv", 2)
