# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Libevent(AutotoolsPackage):
    """The libevent API provides a mechanism to execute a callback function
    when a specific event occurs on a file descriptor or after a
    timeout has been reached. Furthermore, libevent also support
    callbacks due to signals or regular timeouts.

    """

    homepage = "https://libevent.org"
    url = "https://github.com/libevent/libevent/releases/download/release-2.1.8-stable/libevent-2.1.8-stable.tar.gz"
    list_url = "https://libevent.org/old-releases.html"



    variant(
        "openssl", default=True, description="Build with encryption enabled at the libevent level."
    )

    depends_on("c", type="build")  # generated

    depends_on("openssl", when="+openssl")

    conflicts("+openssl", when="@:2.0")

    def url_for_version(self, version):
        if version >= Version("2.0.22"):
            url = "https://github.com/libevent/libevent/releases/download/release-{0}-stable/libevent-{0}-stable.tar.gz"
        else:
            url = "https://github.com/downloads/libevent/libevent/libevent-{0}-stable.tar.gz"

        return url.format(version)

    @property
    def libs(self):
        libs = find_libraries("libevent", root=self.prefix, shared=True, recursive=True)
        return LibraryList(libs)

    def configure_args(self):
        spec = self.spec
        configure_args = []
        if spec.satisfies("+openssl"):
            configure_args.append("--enable-openssl")
        else:
            configure_args.append("--disable-openssl")

        return configure_args

    def patch(self):
        if self.spec.satisfies("%nvhpc"):
            # Remove incompatible compiler flags
            filter_file(" -Wmissing-declarations", "", "configure")
            filter_file(" -Wbad-function-cast", "", "configure")
            filter_file(" -Wno-unused-parameter", "", "configure")
            filter_file(" -Wmissing-field-initializers", "", "configure")
            filter_file(" -Waddress", "", "configure")
            filter_file(" -Wnormalized=id", "", "configure")
            filter_file(" -Woverride-init", "", "configure")
            filter_file(" -Wlogical-op", "", "configure")
