# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.rocm import ROCmPackage

from spack.package import *


class Kokkos(CMakePackage, CudaPackage, ROCmPackage):
    """Kokkos implements a programming model in C++ for writing performance
    portable applications targeting all major HPC platforms."""

    homepage = "https://github.com/kokkos/kokkos"
    git = "https://github.com/kokkos/kokkos.git"
    url = "https://github.com/kokkos/kokkos/releases/download/4.4.01/kokkos-4.4.01.tar.gz"

    tags = ["e4s"]

    test_requires_compiler = True






    with when("@5:"):
        conflicts("%msvc@:19.2")
    depends_on("cmake@3.22:", type="build", when="@5:")
    depends_on("cmake@3.25.2:", type="build", when="@5: +cuda +cmake_lang")
    conflicts("^cmake@3.28", when="@:4.2.01 +cuda")

    devices_variants = {
        "cuda": [False, "Whether to build CUDA backend"],
        "openmp": [False, "Whether to build OpenMP backend"],
        "threads": [False, "Whether to build the C++ threads backend"],
        "serial": [False, "Whether to build serial backend"],
        "rocm": [False, "Whether to build HIP backend"],
        "sycl": [False, "Whether to build the SYCL backend"],
        "openmptarget": [False, "Whether to build the OpenMPTarget backend"],
    }
    requires(
        "+serial", when="~hpx ~openmp ~threads", msg="Kokkos requires at least one host backend"
    )

    tpls_variants = {
        "hpx": [False, None, "Whether to enable the HPX library"],
        "hwloc": [False, None, "Whether to enable the HWLOC library"],
        "numactl": [False, "@:4", "Whether to enable the LIBNUMA library"],
        "memkind": [False, "@:4", "Whether to enable the MEMKIND library"],
    }

    options_variants = {
        "aggressive_vectorization": [False, None, "Aggressively vectorize loops"],
        "atomics_bypass": [
            False,
            "@4.6: +serial~threads~cuda~rocm~hpx~openmp~sycl~openmptarget",
            "Make atomics non-atomic for non-threaded MPI-only use cases",
        ],
        "compiler_warnings": [False, "@:4", "Print all compiler warnings"],
        "complex_align": [True, None, "Align complex numbers"],
        "cuda_constexpr": [False, "+cuda", "Activate experimental constexpr features"],
        "cuda_lambda": [False, "@:4 +cuda", "Activate experimental lambda features"],
        "cuda_ldg_intrinsic": [False, "@:4 +cuda", "Use CUDA LDG intrinsics"],
        "cuda_relocatable_device_code": [False, "+cuda", "Enable RDC for CUDA"],
        "hip_relocatable_device_code": [False, None, "Enable RDC for HIP"],
        "sycl_relocatable_device_code": [False, "@4.5: +sycl", "Enable RDC for SYCL"],
        "cuda_uvm": [False, "@:4 +cuda", "Enable unified virtual memory (UVM) for CUDA"],
        "debug": [False, None, "Activate extra debug features - may increase compiletimes"],
        "debug_bounds_check": [False, None, "Use bounds checking - will increase runtime"],
        "debug_dualview_modify_check": [False, "@:4", "Debug check on dual views"],
        "deprecated_code": [False, "@:4", "Whether to enable deprecated code"],
        "examples": [False, "@:4", "Whether to build examples"],
        "hpx_async_dispatch": [False, "@:4", "Whether HPX supports asynchronous dispath"],
        "tuning": [False, None, "Create bindings for tuning tools"],
        "tests": [False, None, "Build for tests"],
    }

    conflicts("~debug_dualview_modify_check", when="@4.7:")  # always enable from 4.7.00

    spack_micro_arch_map = {
        "thunderx2": "THUNDERX2",
        "zen": "ZEN",
        "zen2": "ZEN2",
        "zen3": "ZEN3",
        "zen4": "ZEN4",
        "zen5": "ZEN5",
        "steamroller": "KAVERI",
        "excavator": "CARIZO",
        "power7": "POWER7",
        "power8": "POWER8",
        "power9": "POWER9",
        "power8le": "POWER8",
        "power9le": "POWER9",
        "sandybridge": "SNB",
        "haswell": "HSW",
        "mic_knl": "KNL",
        "cannonlake": "SKX",
        "cascadelake": "SKX",
        "westmere": "WSM",
        "ivybridge": "SNB",
        "broadwell": "BDW",
        "skylake": "SKL",
        "icelake": "ICL",
        "skylake_avx512": "SKX",
        "sapphirerapids": "SPR",
    }

    spack_cuda_arch_map = {
        "30": "kepler30",
        "32": "kepler32",
        "35": "kepler35",
        "37": "kepler37",
        "50": "maxwell50",
        "52": "maxwell52",
        "53": "maxwell53",
        "60": "pascal60",
        "61": "pascal61",
        "70": "volta70",
        "72": "volta72",
        "75": "turing75",
        "80": "ampere80",
        "86": "ampere86",
        "87": "ampere87",
        "89": "ada89",
        "90": "hopper90",
        "100": "blackwell100",
        "120": "blackwell120",
    }
    cuda_arches = spack_cuda_arch_map.values()
    conflicts("+cuda", when="cuda_arch=none")

    # Kokkos support only one cuda_arch at a time
    variant(
        "cuda_arch",
        description="CUDA architecture",
        values=("none",) + CudaPackage.cuda_arch_values,
        default="none",
        multi=False,
        sticky=True,
        when="+cuda",
    )

    # Since Kokkos supports only one amdgpu_target at a time, the multi-value property is disabled.
    variant(
        "amdgpu_target",
        description="AMD GPU architecture",
        values=("none",) + ROCmPackage.amdgpu_targets,
        default="none",
        multi=False,
        sticky=True,
        when="+rocm",
    )

    amdgpu_arch_map = {
        "gfx900": "vega900",
        "gfx906": "vega906",
        "gfx908": "vega908",
        "gfx90a": "vega90A",
        "gfx940": "amd_gfx940",
        "gfx942": "amd_gfx942",
        "gfx1030": "navi1030",
        "gfx1100": "navi1100",
    }
    amdgpu_apu_arch_map = {"gfx942": "amd_gfx942_apu"}
    amd_support_conflict_msg = (
        "{0} is not supported; "
        "Kokkos supports the following AMD GPU targets: " + ", ".join(amdgpu_arch_map.keys())
    )
    amd_apu_support_conflict_msg = (
        "{0} is not supported; "
        "Kokkos supports the following AMD GPU targets with unified memory: "
        + ", ".join(amdgpu_apu_arch_map.keys())
    )
    for arch in ROCmPackage.amdgpu_targets:
        if arch not in amdgpu_arch_map:
            conflicts(
                "+rocm", when=f"amdgpu_target={arch}", msg=amd_support_conflict_msg.format(arch)
            )
        if arch not in amdgpu_apu_arch_map:
            conflicts(
                "+rocm+apu",
                when=f"amdgpu_target={arch}",
                msg=amd_apu_support_conflict_msg.format(arch),
            )

    intel_gpu_arches = (
        "intel_gen",
        "intel_gen9",
        "intel_gen11",
        "intel_gen12lp",
        "intel_dg1",
        "intel_dg2",
        "intel_xehp",
        "intel_pvc",
    )
    variant(
        "intel_gpu_arch",
        default="none",
        values=("none",) + intel_gpu_arches,
        description="Intel GPU architecture",
    )
    variant("apu", default=False, description="Enable APU support", when="@4.5: +rocm")

    for dev, (dflt, desc) in devices_variants.items():
        variant(dev, default=dflt, description=desc)
    conflicts("+cuda", when="+rocm", msg="CUDA and ROCm are not compatible in Kokkos.")
    depends_on("intel-oneapi-dpl", when="+sycl")
    depends_on("rocthrust", when="@4.3: +rocm")

    for opt, (dflt, when, desc) in options_variants.items():
        variant(opt, default=dflt, description=desc, when=when)

    for tpl, (dflt, when, desc) in tpls_variants.items():
        variant(tpl, default=dflt, description=desc, when=when)
        depends_on(tpl, when="+%s" % tpl)

    variant("wrapper", default=False, description="Use nvcc-wrapper for CUDA build")
    variant("cmake_lang", default=False, description="Use CMake language support for CUDA/HIP")
    depends_on("kokkos-nvcc-wrapper", when="+wrapper")
    depends_on("kokkos-nvcc-wrapper@develop", when="@develop+wrapper")
    conflicts("+wrapper", when="~cuda")
    conflicts("+wrapper", when="+cmake_lang")

    with default_args(multi=False, description="C++ standard"):
        variant("cxxstd", default="17", values=("14", "17", "20"), when="@3")
        variant("cxxstd", default="17", values=("17", "20", "23"), when="@4")
        variant("cxxstd", default="20", values=("20", "23"), when="@5:")
    variant("pic", default=False, description="Build position independent code")

    conflicts("+cuda", when="cxxstd=17 ^cuda@:10")
    conflicts("+cuda", when="cxxstd=20 ^cuda@:11")

    # Expose a way to disable CudaMallocAsync that can cause problems
    # with some MPI such as cray-mpich
    variant("alloc_async", default=False, description="Use CudaMallocAsync", when="@4.2: +cuda")

    # SYCL and OpenMPTarget require C++17 or higher
    conflicts("+sycl", when="cxxstd=14", msg="SYCL requires C++17 or higher")
    conflicts("+openmptarget", when="cxxstd=14", msg="OpenMPTarget requires C++17 or higher")

    # HPX should use the same C++ standard
    for cxxstd in ["14", "17", "20", "23"]:
        depends_on(f"hpx cxxstd={cxxstd}", when=f"+hpx cxxstd={cxxstd}")

    # HPX version constraints
    depends_on("hpx@1.7:", when="+hpx")

    # Patches
    patch("sycl_bhalft_test.patch", when="@4.2.00 +sycl")
    patch(
        "https://github.com/rbberger/kokkos/commit/293319c5844f4d8eea51eb9cd1457115a5016d3f.patch?full_index=1",
        sha256="145619e87dbf26b66ea23e76906576e2a854a3b09f2a2dd70363e61419fa6a6e",
        when="@4.2.00",
    )
    # Remove unnecessary C and C++ languages dependency in scripts/spack_test/CMakeLists.txt (upstreamed in https://github.com/kokkos/kokkos/pull/8357)
    patch(
        "https://github.com/kokkos/kokkos/commit/05d4901538251fff7ae6e58c84db670ad326b5c8.patch?full_index=1",
        sha256="89eb693ad4913c4fd06b25d786d56bfa631d7d612df80c0f5331852e358e0608",
        when="@:4.4",
    )

    variant("shared", default=True, description="Build shared libraries")
    for backend_name in ("cuda", "hip", "sycl"):
        conflicts("+shared", when=f"+{backend_name}_relocatable_device_code")

    # Filter spack-generated files that may include links to the
    # spack compiler wrappers
    filter_compiler_wrappers("kokkos_launch_compiler", relative_root="bin")
    filter_compiler_wrappers(
        "KokkosConfigCommon.cmake", relative_root=os.path.join("lib64", "cmake", "Kokkos")
    )

    # sanity check
    sanity_check_is_file = [
        join_path("include", "KokkosCore_config.h"),
        join_path("include", "Kokkos_Core.hpp"),
    ]
    sanity_check_is_dir = ["bin", "include"]

    @classmethod
    def get_microarch(cls, target):
        """Get the Kokkos microarch name for a Spack target (spec.target)."""
        smam = cls.spack_micro_arch_map

        # Find closest ancestor that has a known microarch optimization
        if target.name not in smam:
            for target in target.ancestors:
                if target.name in smam:
                    break
            else:
                # No known microarch optimizatinos
                return None

        return smam[target.name]

    def append_args(self, cmake_prefix, cmake_options, spack_options):
        variant_to_cmake_option = {"rocm": "hip"}
        for variant_name in cmake_options:
            opt = variant_to_cmake_option.get(variant_name, variant_name)
            optname = f"Kokkos_{cmake_prefix}_{opt.upper()}"
            # Explicitly enable or disable
            option = self.define_from_variant(optname, variant_name)
            if option:
                spack_options.append(option)

    @property
    def kokkos_cxx(self) -> str:
        if self.spec.satisfies("+wrapper"):
            return self["kokkos-nvcc-wrapper"].kokkos_cxx
        # Assumes build-time globals have been set already
        return spack_cxx

    def cmake_args(self):
        spec = self.spec
        from_variant = self.define_from_variant

        if spec.satisfies("~wrapper+cuda") and not (
            spec.satisfies("%clang") or spec.satisfies("%cce") or spec.satisfies("+cmake_lang")
        ):
            raise InstallError(
                "Kokkos requires +wrapper when using +cuda without %clang, %cce or +cmake_lang"
            )

        options = [
            from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"),
            from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            from_variant("BUILD_SHARED_LIBS", "shared"),
            from_variant("Kokkos_ENABLE_COMPILE_AS_CMAKE_LANGUAGE", "cmake_lang"),
        ]

        spack_microarches = []
        if spec.satisfies("+cuda"):
            cuda_arch = spec.variants["cuda_arch"].value
            if cuda_arch != "none":
                kokkos_arch_name = self.spack_cuda_arch_map[cuda_arch]
                spack_microarches.append(kokkos_arch_name)

        kokkos_microarch_name = self.get_microarch(spec.target)
        if kokkos_microarch_name:
            spack_microarches.append(kokkos_microarch_name)

        if spec.satisfies("+rocm"):
            amdgpu_target = spec.variants["amdgpu_target"].value
            if amdgpu_target != "none":
                if amdgpu_target in self.amdgpu_arch_map:
                    if spec.satisfies("+apu") and amdgpu_target in self.amdgpu_apu_arch_map:
                        spack_microarches.append(self.amdgpu_apu_arch_map[amdgpu_target])
                    else:
                        spack_microarches.append(self.amdgpu_arch_map[amdgpu_target])
                else:
                    # Note that conflict declarations should prevent
                    # choosing an unsupported AMD GPU target
                    raise SpackError("Unsupported target: {0}".format(amdgpu_target))

        if self.spec.variants["intel_gpu_arch"].value != "none":
            spack_microarches.append(self.spec.variants["intel_gpu_arch"].value)

        for arch in spack_microarches:
            options.append(self.define("Kokkos_ARCH_" + arch.upper(), True))

        self.append_args("ENABLE", self.devices_variants.keys(), options)
        self.append_args("ENABLE", self.options_variants.keys(), options)
        self.append_args("ENABLE", self.tpls_variants.keys(), options)

        for tpl in self.tpls_variants:
            if spec.satisfies(f"+{tpl}"):
                options.append(self.define(tpl + "_DIR", spec[tpl].prefix))

        if self.spec.satisfies("+wrapper"):
            options.append(self.define("CMAKE_CXX_COMPILER", self.kokkos_cxx))
        elif "+rocm" in self.spec:
            if "+cmake_lang" in self.spec:
                if self.spec.satisfies("%cxx=clang"):
                    options.append(self.define("CMAKE_HIP_COMPILER", self.compiler.cxx))
                else:
                    options.append(
                        self.define(
                            "CMAKE_HIP_COMPILER",
                            join_path(self.spec["llvm-amdgpu"].prefix.bin, "amdclang++"),
                        )
                    )
                options.append(from_variant("CMAKE_HIP_STANDARD", "cxxstd"))
                options.append(
                    self.define(
                        "CMAKE_HIP_ARCHITECTURES", self.spec.variants["amdgpu_target"].value
                    )
                )
                options.append(self.define("CMAKE_HIP_EXTENSIONS", False))
            else:
                options.append(self.define("CMAKE_CXX_COMPILER", self.spec["hip"].hipcc))
            options.append(self.define("Kokkos_ENABLE_ROCTHRUST", True))
        elif "+cuda" in self.spec and "+cmake_lang" in self.spec:
            if self.spec.satisfies("%cxx=clang"):
                options.append(self.define("CMAKE_CUDA_COMPILER", self.compiler.cxx))
            else:
                options.append(
                    self.define(
                        "CMAKE_CUDA_COMPILER", join_path(self.spec["cuda"].prefix.bin, "nvcc")
                    )
                )
            options.append(
                self.define("CMAKE_CUDA_ARCHITECTURES", self.spec.variants["cuda_arch"].value)
            )
            options.append(from_variant("CMAKE_CUDA_STANDARD", "cxxstd"))
            options.append(self.define("CMAKE_CUDA_EXTENSIONS", False))

        if self.spec.satisfies("%oneapi") or self.spec.satisfies("%intel"):
            options.append(self.define("CMAKE_CXX_FLAGS", "-fp-model=precise"))

        options.append(
            self.define_from_variant("Kokkos_ENABLE_IMPL_CUDA_MALLOC_ASYNC", "alloc_async")
        )

        if self.version == Version("4.7.00"):
            options.append(self.define("Kokkos_ENABLE_IMPL_VIEW_LEGACY", True))

        # Remove duplicate options
        return dedupe(options)

    test_script_relative_path = join_path("scripts", "spack_test")

    @run_after("install")
    def setup_build_tests(self):
        # Skip if unsupported version
        cmake_source_path = join_path(self.stage.source_path, self.test_script_relative_path)
        if not os.path.exists(cmake_source_path):
            return
        # Copy test
        cmake_out_path = join_path(self.test_script_relative_path, "out")
        cmake_args = [
            cmake_source_path,
            self.define("SPACK_PACKAGE_SOURCE_DIR", self.stage.source_path),
            self.define(
                "SPACK_PACKAGE_TEST_ROOT_DIR", join_path(install_test_root(self), cmake_out_path)
            ),
            self.define("SPACK_PACKAGE_INSTALL_DIR", self.prefix),
        ]
        cmake(*cmake_args)
        cache_extra_test_sources(self, cmake_out_path)

    def test_run(self):
        """Test if kokkos builds and runs"""
        cmake_path = join_path(
            self.test_suite.current_test_cache_dir, self.test_script_relative_path, "out"
        )

        if not os.path.exists(cmake_path):
            raise SkipTest(f"{cmake_path} is missing")

        cmake = self.spec["cmake"].command
        cmake_args = []
        if self.spec.satisfies("+rocm"):
            prefix_paths = ";".join(get_cmake_prefix_path(self))
            cmake_args.append(self.define("CMAKE_PREFIX_PATH", prefix_paths))

        if self.spec.satisfies("+wrapper"):
            cmake_args.append(
                self.define("CMAKE_CXX_COMPILER", self["kokkos-nvcc-wrapper"].kokkos_cxx)
            )
        else:
            cmake_args.append(self.define("CMAKE_CXX_COMPILER", self["cxx"].cxx))

        cmake(cmake_path, *cmake_args)
        cmake("--build", ".")
        cmake("--build", ".", "--target", "test")
