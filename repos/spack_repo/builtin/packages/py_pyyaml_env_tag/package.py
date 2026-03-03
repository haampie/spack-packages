# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyPyyamlEnvTag(PythonPackage):
    """A custom YAML tag for referencing environment variables in YAML files."""

    homepage = "https://github.com/waylan/pyyaml-env-tag"
    pypi = "pyyaml_env_tag/pyyaml_env_tag-0.1.tar.gz"

    license("MIT")

    version("0.1", sha256="70092675bda14fdec33b31ba77e7543de9ddc88f2e5b99160396572d11525bdb")

