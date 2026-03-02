# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Glfw(CMakePackage):
    """GLFW is an Open Source, multi-platform library for
    OpenGL, OpenGL ES and Vulkan development on the desktop. It
    provides a simple API for creating windows, contexts and
    surfaces, receiving input and events."""

    homepage = "https://www.glfw.org/"
    url = "https://github.com/glfw/glfw/archive/3.3.2.tar.gz"

    license("Zlib")

    version("3.2.1", sha256="e10f0de1384d75e6fc210c53e91843f6110d6c4f3afbfb588130713c2f9d8fe8")
    version("3.2", sha256="cb3aab46757981a39ae108e5207a1ecc4378e68949433a2b040ce2e17d8f6aa6")
    version("3.1.2", sha256="6ac642087682aaf7f8397761a41a99042b2c656498217a1c63ba9706d1eef122")
    version("3.1.1", sha256="4de311ec9bf43bfdc8423ddf93b91dc54dc73dcfbedfb0991b6fbb3a9baf245f")
    version("3.1", sha256="2140f4c532e7ce4c84cb7e4c419d0979d5954fa1ce204b7646491bd2cc5bf308")
    version("3.0.4", sha256="a4e7c57db2086803de4fc853bd472ff8b6d2639b9aa16e6ac6b19ffb53958caf")
    version("3.0.3", sha256="7a182047ba6b1fdcda778b79aac249bb2328b6d141188cb5df29560715d01693")

    variant("doc", default=False, description="Build documentation")
    variant("shared", default=False, description="Builds a shared version of the library")

    # dependencies
    depends_on("c", type="build")  # generated

    depends_on("doxygen", type="build", when="+doc")

    depends_on("libxrandr", when="platform=linux")
    depends_on("libxcursor", when="platform=linux")
    depends_on("libxdamage", when="platform=linux")
    depends_on("libxi", when="platform=linux")
    depends_on("libxmu", when="platform=linux")
    depends_on("freetype", when="platform=linux")
    depends_on("fontconfig", when="platform=linux")
    depends_on("pkgconfig", type="build", when="platform=linux")

    def cmake_args(self):
        return [self.define_from_variant("BUILD_SHARED_LIBS", "shared")]
