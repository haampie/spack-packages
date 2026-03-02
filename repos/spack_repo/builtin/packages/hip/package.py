# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Hip(CMakePackage):
    """HIP is a C++ Runtime API and Kernel Language that allows developers to
    create portable applications for AMD and NVIDIA GPUs from
    single source code."""

    homepage = "https://github.com/ROCm/HIP"
    git = "https://github.com/ROCm/HIP.git"
    url = "https://github.com/ROCm/HIP/archive/rocm-6.4.3.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath", "haampie", "afzpatel")
    libraries = ["libamdhip64"]

    license("MIT")
    version("7.2.0", sha256="4a22fcd0baf8df47d2e234f887f5bc03d522ce78928f82d1b0669a55897c4205")
    version("7.1.1", sha256="c64b3219237903d6b27944f236930a1024ed17eb5399165875fbf410fcacf6f4")
    version("7.1.0", sha256="e757a6e4a15d4113cd7cd8a4e9a2a3ff7a6a9ccbc65951179419331214f2784a")
    version("7.0.2", sha256="80486998b115e5f61b72913887ccc0507ac332eda4068879bdfb7e3c8611f666")
    version("7.0.0", sha256="762794050eb9f47d8278a3d023bb47fd075c30c91ea9c4719cae55d91535de3c")
    version("6.4.3", sha256="3def2459ca9258f04d35d1d3b0173237cea2b963814886bb8af6a0e317718d3d")
    version("6.4.2", sha256="27e3558ecafa9a7471441aabdd870648fa2619147caa721bd98514fa00d246c1")
    version("6.4.1", sha256="f26f098b08504636c6f4e1da45b162f1df2ce6608eba85606fa7932d8fea960f")
    version("6.4.0", sha256="bec899ba67df9aa7056297e5ad104b8e36938b1bab22f1f418f69a8e0043d07f")
    version("6.3.3", sha256="aa3a5466304d1dbee0d976b50fccb710dd12e2e1d5534793396447c0ff845e2c")
    version("6.3.2", sha256="66a4eba98bd74fc7126ce7cb4d59653b22075fe95a70412fe283dc806ae366e0")
    version("6.3.1", sha256="76f862493c4912a06e0e0b8da3917c2ba7481f1e05f2c23ffd5e05f8c44e3037")
    version("6.3.0", sha256="950bfaf108a0af44eb169646f81f564f75f49e974acd06139b77245cfd327267")
    version("6.2.4", sha256="7a88edd689230b422250852a391b3b377b4371bbaef1e4f36d7fb699fcb0562b")
    version("6.2.1", sha256="1f130fa8d0a60cfb3560892c50ed7c57902b1398b21d3168f4be2d7ee512da96")
    version("6.2.0", sha256="95de10ef1815e8076a94a53bae3752dfd0e9f0abe513ca3fb79969773cff12d4")
    version("6.0.0", sha256="ba8ce0d0960b260ff44ab47da58f98b8df9b659835aa62e32e018a63379bbc79")
    version("5.7.1", sha256="ea34c75d2cff366fcdd45109c5be460a48d4fcf72b8a534368b54eae5d05db0e")
    version("5.7.0", sha256="8974a436e7f1daf232a77e27a215bcb24a8cc132aa11b5b885a7417ad4246074")

    variant("rocm", default=True, description="Enable ROCm support")
    variant("cuda", default=False, description="Build with CUDA")
    variant("asan", default=False, description="Build with address-sanitizer enabled or disabled")
    conflicts("+cuda +rocm", msg="CUDA and ROCm support are mutually exclusive")
    conflicts("~cuda ~rocm", msg="CUDA or ROCm support is required")
    conflicts("~rocm +asan", msg="ROCm must be enabled for asan")

    conflicts("+asan", when="os=rhel9")
    conflicts("+asan", when="os=centos7")
    conflicts("+asan", when="os=centos8")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cuda", when="+cuda")


    test_requires_compiler = True

    with when("+rocm"):
        depends_on("py-cppheaderparser", type="build")
        depends_on("libx11", when="+asan")
        depends_on("xproto", when="+asan")
        # hipcc likes to add `-lnuma` by default :(
        # ref https://github.com/ROCm/HIP/pull/2202
        depends_on("numactl")

        for ver in [
            "5.7.0",
            "5.7.1",
            "6.0.0",
            "6.0.2",
            "6.1.0",
            "6.1.1",
            "6.1.2",
            "6.2.0",
            "6.2.1",
            "6.2.4",
        ]:
            depends_on(f"hsakmt-roct@{ver}", when=f"@{ver}")

        for ver in [
            "5.7.0",
            "5.7.1",
            "6.0.0",
            "6.0.2",
            "6.1.0",
            "6.1.1",
            "6.1.2",
            "6.2.0",
            "6.2.1",
            "6.2.4",
            "6.3.0",
            "6.3.1",
            "6.3.2",
            "6.3.3",
            "6.4.0",
            "6.4.1",
            "6.4.2",
            "6.4.3",
            "7.0.0",
            "7.0.2",
            "7.1.0",
            "7.1.1",
            "7.2.0",
        ]:
            depends_on(f"hsa-rocr-dev@{ver}", when=f"@{ver}")
            depends_on(f"comgr@{ver}", when=f"@{ver}")
            depends_on(f"llvm-amdgpu@{ver} +rocm-device-libs", when=f"@{ver}")
            depends_on(f"rocminfo@{ver}", when=f"@{ver}")
            depends_on(f"roctracer-dev-api@{ver}", when=f"@{ver}")
            depends_on(f"hipify-clang@{ver}", when=f"@{ver}")
            depends_on(f"rocm-core@{ver}", when=f"@{ver}")
    for ver in [
        "6.0.0",
        "6.0.2",
        "6.1.0",
        "6.1.1",
        "6.1.2",
        "6.2.0",
        "6.2.1",
        "6.2.4",
        "6.3.0",
        "6.3.1",
        "6.3.2",
        "6.3.3",
        "6.4.0",
        "6.4.1",
        "6.4.2",
        "6.4.3",
        "7.0.0",
        "7.0.2",
        "7.1.0",
        "7.1.1",
        "7.2.0",
    ]:
        depends_on(f"hipcc@{ver}", when=f"@{ver}")

    for ver in [
        "6.2.0",
        "6.2.1",
        "6.2.4",
        "6.3.0",
        "6.3.1",
        "6.3.2",
        "6.3.3",
        "6.4.0",
        "6.4.1",
        "6.4.2",
        "6.4.3",
        "7.0.0",
        "7.0.2",
        "7.1.0",
        "7.1.1",
        "7.2.0",
    ]:
        depends_on(f"rocprofiler-register@{ver}", when=f"@{ver}")

    # roc-obj-ls requirements
    depends_on("perl-file-which")
    depends_on("perl-uri-encode")

    # Add hip-clr sources thru the below
    for d_version, d_shasum in [
        ("7.1.1", "b09539ef53a775c03352f9843f3a346e4f2ad3941c1954e953d352e4984ee708"),
        ("7.1.0", "d53ee72dd430c934a53b1fe5c798ac34c53e8826589f8f9f214419512059ad2d"),
        ("7.0.2", "b49b1ccbf86ef78f4da5ff13ec3ee94f6133c55db3a95b823577b0808db5f2f1"),
        ("7.0.0", "cc417e73cda903511db5a72b77704fd41bf7b39204c5cacb2c64701b344b8c5d"),
        ("6.4.3", "aa7c9d9d7da3b5fc944b17ca7c032e8924a8dc327ec79eb8cb7f0c9df6fa76dc"),
        ("6.4.2", "6dca1ffff36dbf8665594a72b47b8dd0362f7ee446dea03961d8b5a639bf3ede"),
        ("6.4.1", "18ee75a04f6fc55e72f8b3fcad1e0d58eceb2ce0e0696ca76d9b3dfaf4bfd7ff"),
        ("6.4.0", "76fd0ad83da0dabf7c91ca4cff6c51f2be8ab259e08ad9743af47d1b3473c2ff"),
        ("6.3.3", "8e5adca8f8c2d99d4a4e49605dd6b56b7881b762ee8ce15b4a7000e3cd982fec"),
        ("6.3.2", "ec13dc4ffe212beee22171cb2825d2b16cdce103c835adddb482b9238cf4f050"),
        ("6.3.1", "bfb8a4a59e7bd958e2cd4bf6f14c6cdea601d9827ebf6dc7af053a90e963770f"),
        ("6.3.0", "829e61a5c54d0c8325d02b0191c0c8254b5740e63b8bfdb05eec9e03d48f7d2c"),
        ("6.2.4", "0a3164af7f997a4111ade634152957378861b95ee72d7060eb01c86c87208c54"),
        ("6.2.1", "e9cff3a8663defdbda833d49c9e7160171eca14dc285ffe4061378607d6c890d"),
        ("6.2.0", "620e4c6a7f05651cc7a170bc4700fef8cae002420307a667c638b981d00b25e8"),
        ("6.1.2", "1a1e21640035d957991559723cd093f0c7e202874423667d2ba0c7662b01fea4"),
        ("6.1.1", "2db02f335c9d6fa69befcf7c56278e5cecfe3db0b457eaaa41206c2585ef8256"),
        ("6.1.0", "49b23eef621f4e8e528bb4de8478a17436f42053a2f7fde21ff221aa683205c7"),
        ("6.0.2", "cb8ac610c8d4041b74fb3129c084f1e7b817ce1a5a9943feca1fa7531dc7bdcc"),
        ("6.0.0", "798b55b5b5fb90dd19db54f136d8d8e1da9ae1e408d5b12b896101d635f97e50"),
        ("5.7.1", "c78490335233a11b4d8a5426ace7417c555f5e2325de10422df06c0f0f00f7eb"),
        ("5.7.0", "bc2447cb6fd86dff6a333b04e77ce85755104d9011a14a044af53caf02449573"),
    ]:
        resource(
            name="clr",
            url=f"https://github.com/ROCm/clr/archive/refs/tags/rocm-{d_version}.tar.gz",
            sha256=d_shasum,
            expand=True,
            destination="",
            placement="clr",
            when=f"@{d_version}",
        )

        # For avx build, the start address of values_ buffer in KernelParameters is not
        # correct as it is computed based on 16-byte alignment.
        patch(
            "https://github.com/ROCm/clr/commit/c4f773db0b4ccbbeed4e3d6c0f6bff299c2aa3f0.patch?full_index=1",
            sha256="5bb9b0e08888830ccf3a0a658529fe25f4ee62b5b8890f349bf2cc914236eb2f",
            working_dir="clr",
            when="@5.7:6.0",
        )
        patch(
            "https://github.com/ROCm/clr/commit/7868876db742fb4d44483892856a66d2993add03.patch?full_index=1",
            sha256="7668b2a710baf4cb063e6b00280fb75c4c3e0511575e8298a9c7ae5143f60b33",
            working_dir="clr",
            when="@5.7:6.0",
        )

    for d_version, d_shasum in [
        ("7.2.0", "728ea7e9bf16e6ed217a0fd1a8c9afaba2dae2e7908fa4e27201e67c803c5638")
    ]:
        resource(
            name="rocm-systems",
            url=f"https://github.com/ROCm/rocm-systems/archive/rocm-{d_version}.tar.gz",
            sha256=d_shasum,
            expand=True,
            destination="",
            placement="rocm-systems",
            when=f"@{d_version}",
        )

    # Add hipcc sources thru the below
    for d_version, d_shasum in [
        ("5.7.1", "d47d27ef2b5de7f49cdfd8547832ac9b437a32e6fc6f0e9c1646f4b704c90aee"),
        ("5.7.0", "9f839bf7226e5e26f3150f8ba6eca507ab9a668e68b207736301b3bb9040c973"),
    ]:
        resource(
            name="hipcc",
            url=f"https://github.com/ROCm/HIPCC/archive/refs/tags/rocm-{d_version}.tar.gz",
            sha256=d_shasum,
            expand=True,
            destination="",
            placement="hipcc",
            when=f"@{d_version}",
        )
    # Add hipother sources thru the below
    for d_version, d_shasum in [
        ("7.1.1", "abf5ad4e94aa2d504b4f6d0279780066f3d9a07518fa8b5af0edeac2a6b69d41"),
        ("7.1.0", "076e8deba8a6db67bda7d97da8c2395d2a698d968a9cda5bda43ce65cce015ed"),
        ("7.0.2", "90ba233cc5242a2b3d2f4b4576b9d61f78bbf13f648e713a377b10df00257592"),
        ("7.0.0", "611aa99b4fe88988850e4533056ebfede1cb546ca2f208dbf3eda84b041ef6d6"),
        ("6.4.3", "bf5112a7dbc62ba292d782297edebb385b18563f4efebfb4b581230f9383a89f"),
        ("6.4.2", "c2828018e6241bf0464c38f63e16abeab0e8eb861f052454b2d1bc96e0bae66a"),
        ("6.4.1", "2251976146b65a5bdda5a46bfecf323d8dd122104a96394b0e76b35060a10842"),
        ("6.4.0", "53d5654d34e00f4bfa0846b291fe87ef6d43087349917159e663a842ea29a783"),
        ("6.3.3", "95cb2aab4bd996f0bd5f38427412cd768692a11fad70b97d20e402f32b1ef03e"),
        ("6.3.2", "1623d823de49471aae3ecb1fad0e9cdddf9301a4089f1fd44f78ac2ff0c20fb2"),
        ("6.3.1", "caa69147227bf72fa7b076867f84579456ef55af63efec29914265a80602df42"),
        ("6.3.0", "a28eb1e8fe239b41e744584d45d676925ca210968ecb21bfa60678cf8e86eeb7"),
        ("6.2.4", "b7ebcf8a2679e50d27c49ebec0dbea5a67573f8b8c3f4a29108c84b28b5bedee"),
        ("6.2.1", "5d99e498c1fece44a421574282fc89c6a2499979eaa9f850e5caa7fa3a8938b8"),
        ("6.2.0", "1f854b0c07d71b10450080e3bbffe47adaf10a9745a9212797d991756a100174"),
        ("6.1.2", "2740d1e3dcf1f2d07d2a8db6acf4c972941ae392172b83fd8ddcfe8706a40d0b"),
        ("6.1.1", "8b975623c8ed1db53feea2cfd5d29f2a615e890aee1157d0d17adeb97200643f"),
        ("6.1.0", "43a48ccc82f705a15852392ee7419e648d913716bfc04063a53d2d17979b1b46"),
        ("6.0.2", "0bebb3774debcecc0b29a0cc5aa98e373a3ee7acf161503d0d9c9d0ecc8b8010"),
        ("6.0.0", "d3bf62cc17c3c44fea52b34bcbf725e7af1afc3542c2884cefcd41f65371f552"),
    ]:
        resource(
            name="hipother",
            url=f"https://github.com/ROCm/hipother/archive/refs/tags/rocm-{d_version}.tar.gz",
            sha256=d_shasum,
            expand=True,
            destination="",
            placement="hipother",
            when=f"@{d_version} +cuda",
        )

    # Improve compilation without git repo and remove compiler rt linkage
    # for host and correction in CMake target path variable and
    # correcting the CMake path variable.
    patch("0014-Remove-compiler-rt-linkage-for-host-for-5.7.0.patch", when="@5.7.0:5.7")
    patch("0014-remove-compiler-rt-linkage-for-host.6.0.patch", when="@6.0")
    patch("0014-remove-compiler-rt-linkage-for-host.6.1.patch", when="@6.1")
    patch("0015-reverting-operator-mixup-fix-for-slate.patch", when="@:6.0")

    # See https://github.com/ROCm/HIP/pull/3206

