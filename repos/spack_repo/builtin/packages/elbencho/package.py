# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class Elbencho(MakefilePackage):
    """
    Elbencho storage benchmark
    """

    homepage = "https://github.com/breuner/elbencho"
    url = "https://github.com/breuner/elbencho/archive/refs/tags/v3.0-1.tar.gz"
    git = "https://github.com/breuner/elbencho.git"



    version("2.2-5", sha256="4b598639452665a8b79c4c9d8a22ae63fb9b04057635a45e686aa3939ee255b4")

    variant("s3", default=False, description="Enable support for s3 api")
    variant("cuda", default=True, description="Enable CUDA support", when="+cufile")
    variant("cuda", default=False, description="Enable CUDA support")
    variant("cufile", default=False, description="GPU Direct Storage")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cuda", when="+cuda")
    depends_on(
        """
           boost
           +filesystem+program_options
           +thread
           +system+date_time
           +regex
           +serialization
           +iostreams
        """
    )
    depends_on("ncurses")
    depends_on("numactl")
    depends_on("libaio")
    depends_on("curl", when="+s3")
    depends_on("libarchive", when="+s3")
    depends_on("openssl", when="+s3")
    depends_on("uuid", when="+s3")
    depends_on("zlib", when="+s3")
    depends_on("cmake", when="+s3")

    conflicts("+cufile", when="~cuda")

    def edit(self, spec, prefix):
        os.mkdir(prefix.bin)
        os.environ["INST_PATH"] = prefix.bin
        if spec.satisfies("+s3"):
            os.environ["S3_SUPPORT"] = "1"
        if spec.satisfies("+cuda"):
            os.environ["CUDA_SUPPORT"] = "1"
        if spec.satisfies("+cufile"):
            os.environ["CUFILE_SUPPORT"] = "1"
        makefile = FileFilter("Makefile")
        makefile.filter(r"\s+/etc/bash_completion.d/", f" {prefix}/etc/bash_completion.d/")
        makefile.filter(r"-lncurses", "-ltinfo -lncurses")
