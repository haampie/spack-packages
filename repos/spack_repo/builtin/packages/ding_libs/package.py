# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class DingLibs(AutotoolsPackage):
    """A meta-package that pulls in libcollection, libdhash, libini_config,
    librefarray libbasicobjects, and libpath_utils."""

    homepage = "https://pagure.io/SSSD/ding-libs"
    url = "https://releases.pagure.org/SSSD/ding-libs/ding-libs-0.6.1.tar.gz"

    version("0.5.0", sha256="dab937537a05d7a7cbe605fdb9b3809080d67b124ac97eb321255b35f5b172fd")

    depends_on("c", type="build")  # generated
