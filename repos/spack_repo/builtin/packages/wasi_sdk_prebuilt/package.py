# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin.build_systems.generic import Package

from spack.package import *


class WasiSdkPrebuilt(Package):
    """
    A group of standard API specifications for software compiled to the W3C WebAssembly standard
    """

    homepage = "https://wasi.dev/"
    url = "https://github.com/WebAssembly/wasi-sdk/releases/download/wasi-sdk-14/wasi-sdk-14.0-linux.tar.gz"

    maintainers("teaguesterling")

    license("APACHE-2.0", checked_by="teaguesterling")

    version("25.0", sha256="52640dde13599bf127a95499e61d6d640256119456d1af8897ab6725bcf3d89c")
    version("24.0", sha256="c6c38aab56e5de88adf6c1ebc9c3ae8da72f88ec2b656fb024eda8d4167a0bc5")
    version("23.0", sha256="521838d92816c92a731dee9246b0364eb00e300c5e2336e6dfa38f26a6494b06")
    version("17.0", sha256="8778a476af7898a51db9b78395687cc9c8b69702850da77a763711e832614dac")
    version("16.0", sha256="10df3418485e60b9283c1132102f8d3ca34b4fbe8c4649e30282ee84fe42d788")
    version("15.0", sha256="9b1f2c900a034a44e59b74843cd79b4f189342598e554029367ef0a2ac286703")
    version("14.0", sha256="8c8ebb7f71dcccbb8b1ab384499a53913b0b6d1b7b3281c3d70165e0f002e821")

    provides("wasi-sdk")

    def url_for_version(self, version):
        base = "https://github.com/WebAssembly/wasi-sdk/releases/download"
        major = version.up_to(1)
        full = version.up_to(2)
        return f"{base}/wasi-sdk-{major}/wasi-sdk-{full}-linux.tar.gz"

    def install(self, spec, prefix):
        install_tree("share/wasi-sysroot", prefix)
