# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Filebench(AutotoolsPackage):
    """
    Filebench is a file system and storage benchmark that can generate a
    large variety of workloads. Unlike typical benchmarks it is extremely
    flexible and allows to specify application's I/O behavior using its
    extensive Workload Model Language (WML). Users can either describe
    desired workloads from scratch or use(with or without modifications)
    workload personalities shipped with Filebench(e.g., mail-, web-, file-,
    and database-server workloads). Filebench is equally good for micro
    and macro-benchmarking, quick to setup, and relatively easy to use.
    """

    homepage = "https://github.com/filebench/filebench"
    url = "https://github.com/filebench/filebench/archive/1.4.9.1.tar.gz"



