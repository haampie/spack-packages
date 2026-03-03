# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Enchant(AutotoolsPackage):
    """Enchant is a library (and command-line program) that wraps a
    number of different spelling libraries and programs with a
    consistent interface."""

    homepage = "https://rrthomas.github.io/enchant/"
    url = "https://github.com/rrthomas/enchant/releases/download/v2.8.2/enchant-2.8.2.tar.gz"



    variant("hunspell", default=True, description="Enables hunspell backend")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("pkgconfig", type="build", when="platform=linux")

    depends_on("glib")
    depends_on("aspell")
    depends_on("hunspell", when="+hunspell")
    depends_on("groff", type="build", when="@2.6.7:")

    def configure_args(self):
        spec = self.spec
        args = ["--with-aspell", "--with-aspell-dir={0}".format(spec["aspell"].prefix)]

        args += self.with_or_without("hunspell")
        if spec.satisfies("+hunspell"):
            args.append("--with-hunspell-dir={0}".format(spec["hunspell"].prefix))

        return args
