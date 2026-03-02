# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.perl import PerlPackage

from spack.package import *


class PerlBioEutilities(PerlPackage):
    """BioPerl low-level API for retrieving and storing data from NCBI eUtils"""

    homepage = "https://metacpan.org/pod/Bio::DB::EUtilities"
    url = "https://cpan.metacpan.org/authors/id/C/CJ/CJFIELDS/Bio-EUtilities-1.77.tar.gz"




    depends_on("perl@5.10.0:", type=("build", "link", "run", "test"))
    depends_on("perl-bio-asn1-entrezgene", type=("build", "run", "test"))
    depends_on("perl-bioperl", type=("build", "run", "test"))
    depends_on("perl-http-message", type=("build", "run", "test"))
    depends_on("perl-libwww-perl", type=("build", "run", "test"))
    depends_on("perl-text-csv", type=("build", "run", "test"))
    depends_on("perl-uri", type=("build", "run", "test"))
    depends_on("perl-xml-simple", type=("build", "run", "test"))
