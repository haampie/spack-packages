# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack_repo.builtin.build_systems.meson import MesonPackage

from spack.package import *


class Wayland(MesonPackage, AutotoolsPackage):
    """Wayland is a project to define a protocol for a compositor to talk
    to its clients as well as a library implementation of the protocol.
    The compositor can be a standalone display server running on Linux
    kernel modesetting and evdev input devices, an X application, or a
    wayland client itself.  The clients can be traditional applications,
    X servers(rootless or fullscreen) or other display servers."""

    homepage = "https://wayland.freedesktop.org/"
    url = "https://gitlab.freedesktop.org/wayland/wayland/-/archive/1.18.0/wayland-1.18.0.tar.gz"
    list_url = "https://gitlab.freedesktop.org/wayland/wayland/-/tags"
    git = "https://gitlab.freedesktop.org/wayland/wayland/"

    maintainers("wdconinc")

    build_system(
        conditional("autotools", when="@:1.19"),
        conditional("meson", when="@1.18:"),
        default="meson",
    )

    variant("doc", default=False, description="Build documentation")

    license("MIT")

    version("1.23.1", sha256="158ec49af498f2558c7fbf7e8b070d010d4e270cc6076003a18a6c813f87e244")
    version("1.23.0", sha256="7c5c28fa73f22d1c5021e17e1148f29ab17bf8b776a406f1c4489d3e2992ec3a")
    version("1.22.0", sha256="bbca9c906a8fb8992409ebf51812f19e2a784b2c169d4b784cdd753b4bb448ef")
    version("1.21.0", sha256="53b7fa67142e653820030ec049971bcb5e84ac99e05cba5bcb9cb55f43fae4b3")
    version("1.20.0", sha256="20523cd6f2c18c3c86725467157c6221e19de76fbfad944042a2d494af3c7a92")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    with when("build_system=autotools"):
        depends_on("autoconf", type="build")
        depends_on("automake", type="build")
        depends_on("libtool", type="build")
        depends_on("m4", type="build")

    with when("build_system=meson"):
        depends_on("meson@0.56.0:", type="build")
        depends_on("meson@0.57.0:", type="build", when="@1.23:")

    depends_on("pkgconfig", type="build")
    depends_on("libxml2")
    depends_on("chrpath")
    depends_on("expat")
    depends_on("libffi")

    with when("+doc"):
        depends_on("docbook-xsl", type="build")
        depends_on("doxygen", type="build")
        depends_on("xmlto", type="build")
        depends_on("libxslt", type="build")
        depends_on("graphviz+expat+libgd", type="build")

    @when("build_system=autotools")
    def configure_args(self):
        args = []
        args.extend(self.enable_or_disable("documentation", variant="doc"))
        return args

    @when("build_system=meson")
    def meson_args(self):
        spec = self.spec
        opt_bool = lambda c, o: "-D%s=%s" % (o, str(c).lower())
        args = []
        args.append(opt_bool("+doc" in spec, "documentation"))
        return args
