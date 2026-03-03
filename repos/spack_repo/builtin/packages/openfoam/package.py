from spack.package import *
__all__ = [
]
class Openfoam(Package):
    git = "https://gitlab.com/openfoam/core/openfoam.git"
    version("develop", branch="develop", submodules=True)
    variant(
        "paraview", default=False, description="Build paraview plugins and runtime post-processing"
    )
    depends_on("flex@:2.6.1,2.6.4:")
    depends_on("paraview@:5.0.1", when="@1612+paraview")
