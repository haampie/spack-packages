from spack.package import *
class Openfoam(Package):
    """OpenFOAM is a GPL-opensource C++ CFD-toolbox.
    """
    url = "https://sourceforge.net/projects/openfoam/files/v1906/OpenFOAM-v1906.tgz"
    version("1612", sha256="2909c43506a68e1f23efd0ca6186a6948ae0fc8fe1e39c78cc23ef0d69f3569d")
    variant(
        "paraview", default=False, description="Build paraview plugins and runtime post-processing"
    )
    depends_on("flex@:2.6.1,2.6.4:")
    depends_on("paraview@5.4:", when="@1706:+paraview")
