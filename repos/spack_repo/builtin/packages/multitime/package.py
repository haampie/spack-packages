# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Multitime(AutotoolsPackage):
    """multitime is, in essence, a simple extension to time which runs a
    command multiple times and prints the timing means, standard deviations,
    mins, medians, and maxes having done so. This can give a much better
    understanding of the command's performance."""

    homepage = "https://tratt.net/laurie/src/multitime/"
    url = "https://tratt.net/laurie/src/multitime/releases/multitime-1.4.tar.gz"



    depends_on("c", type="build")  # generated
