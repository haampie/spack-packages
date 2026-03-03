# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class HsaAmdAqlprofile(CMakePackage):
    """Architected Queuing Language Profiling Library
    AQLprofile is an open source library that enables advanced
    GPU profiling and tracing on AMD platforms"""

    homepage = "https://github.com/ROCm/aqlprofile"
    git = "https://github.com/ROCm/rocm-systems"
    tags = ["rocm"]

    def url_for_version(self, version):
        if version <= Version("7.1.1"):
            url = "https://github.com/ROCm/aqlprofile/archive/rocm-{0}.tar.gz"
        else:
            url = "https://github.com/ROCm/rocm-systems/archive/rocm-{0}.tar.gz"
        return url.format(version)


    depends_on("c", type="build")
    depends_on("cxx", type="build")

    for ver in ["7.0.0", "7.0.2", "7.1.0", "7.1.1", "7.2.0"]:
        depends_on(f"hsa-rocr-dev@{ver}", when=f"@{ver}")

    @property
    def root_cmakelists_dir(self):
        if self.spec.satisfies("@:7.1"):
            return "."
        else:
            return "projects/aqlprofile"
