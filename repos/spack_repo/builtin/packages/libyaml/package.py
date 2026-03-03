# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Libyaml(AutotoolsPackage):
    """A C library for parsing and emitting YAML."""

    homepage = "https://pyyaml.org/wiki/LibYAML"
    url = "https://pyyaml.org/download/libyaml/yaml-0.2.4.tar.gz"
    git = "https://github.com/yaml/libyaml.git"


    version("master", branch="master")
    version("0.2.5", sha256="c642ae9b75fee120b2d96c712538bd2cf283228d2337df2cf2988e3c02678ef4")
    version("0.2.4", sha256="d80aeda8747b7c26fbbfd87ab687786e58394a8435ae3970e79cb97882e30557")
    version("0.2.3", sha256="08bbb80284d77092e68a6f69f1e480e8ed93e215c47b2ca29290e3bd5a191108")
    version("0.2.2", sha256="4a9100ab61047fd9bd395bcef3ce5403365cafd55c1e0d0299cde14958e47be9")
    version("0.2.1", sha256="78281145641a080fb32d6e7a87b9c0664d611dcb4d542e90baf731f51cbb59cd")
    version("0.1.7", sha256="8088e457264a98ba451a90b8661fcb4f9d6f478f7265d48322a196cec2480729")
    version("0.1.6", sha256="7da6971b4bd08a986dd2a61353bc422362bd0edcc67d7ebaac68c95f74182749")


    @run_before("configure")
    def bootstrap(self):
        if self.spec.satisfies("@master"):
            bootstrap = Executable("./bootstrap")
            bootstrap()
