# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.perl import PerlPackage

from spack.package import *


class PerlCatalystDevel(PerlPackage):
    """Catalyst Development Tools"""

    homepage = "https://metacpan.org/pod/Catalyst::Devel"
    url = "https://cpan.metacpan.org/authors/id/H/HA/HAARG/Catalyst-Devel-1.42.tar.gz"

    maintainers("EbiArnie")



    depends_on("perl-catalyst-plugin-static-simple@0.28:", type=("build", "run", "test"))
    depends_on("perl-catalyst-runtime", type=("build", "run", "test"))
    depends_on("perl-config-general@2.42:", type=("build", "run", "test"))
    depends_on("perl-file-changenotify@0.07:", type=("build", "run", "test"))
    depends_on("perl-file-copy-recursive", type=("build", "run", "test"))
    depends_on("perl-file-sharedir", type=("build", "run", "test"))
    depends_on("perl-file-sharedir-install", type=("build"))
    depends_on("perl-module-install@1.02:", type=("build", "run", "test"))
    depends_on("perl-moose", type=("build", "run", "test"))
    depends_on("perl-moosex-emulate-class-accessor-fast", type=("build", "run", "test"))
    depends_on("perl-namespace-autoclean", type=("build", "run", "test"))
    depends_on("perl-namespace-clean", type=("build", "run", "test"))
    depends_on("perl-path-class@0.09:", type=("build", "run", "test"))
    depends_on("perl-template-toolkit", type=("build", "run", "test"))
    depends_on("perl-test-fatal@0.003:", type=("build", "test"))
    depends_on("perl-yaml-tiny", type=("build", "test"))
