from spack_repo.builtin.build_systems.generic import Package
from spack_repo.builtin.packages.boost.package import Boost
from spack.package import *
# Not the nice way of doing things, but is a start for refactoring
__all__ = [
    "add_extra_files",
    "write_environ",
    "rewrite_environ_files",
]
# -----------------------------------------------------------------------------
class Openfoam(Package):
    """OpenFOAM is a GPL-opensource C++ CFD-toolbox.
    """
    version("1612", sha256="2909c43506a68e1f23efd0ca6186a6948ae0fc8fe1e39c78cc23ef0d69f3569d")
    variant(
        "paraview", default=False, description="Build paraview plugins and runtime post-processing"
    )
    depends_on("flex@:2.6.1,2.6.4:")
    # Require scotch with ptscotch - corresponds to standard OpenFOAM setup
    depends_on("paraview@5.4:", when="@1706:+paraview")
