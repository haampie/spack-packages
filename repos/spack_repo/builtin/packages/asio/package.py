# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Asio(AutotoolsPackage):
    """C++ library for network and low-level I/O programming."""

    homepage = "https://think-async.com/Asio/"
    url = "https://github.com/chriskohlhoff/asio/archive/asio-1-18-2.tar.gz"
    git = "https://github.com/chriskohlhoff/asio.git"

    # As uneven minor versions of asio are not considered stable, they wont be added anymore


    depends_on("pkgconfig", type="build", when="@1.23:")

    # See https://github.com/chriskohlhoff/asio/issues/944 and
    # https://github.com/chriskohlhoff/asio/pull/995
    conflicts(
        "%gcc@12:",
        msg="asio v1.22.1 fixed missing includes necessary for gcc v12 and above",
    )

    stds = ("11", "14", "17", "20", "23")
    variant(
        "cxxstd",
        default="11",
        values=stds,
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    variant("separate_compilation", default=False, description="Compile Asio sources separately")

    variant("boost_coroutine", default=False, description="Enable support for Boost.Coroutine.")
    variant("boost_regex", default=False, description="Enable support for Boost.Regex.")

    for std in stds:
        depends_on(f"boost +regex cxxstd={std}", when=f"cxxstd={std} +boost_regex")
        depends_on(f"boost +context+coroutine cxxstd={std}", when=f"cxxstd={std} +boost_coroutine")

