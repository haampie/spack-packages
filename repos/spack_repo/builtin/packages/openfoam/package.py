from spack.package import *
class Openfoam(Package):
    """OpenFOAM is a GPL-opensource C++ CFD-toolbox.
    in 2004.
    """
    url = "https://sourceforge.net/projects/openfoam/files/v1906/OpenFOAM-v1906.tgz"
    version("1612", sha256="2909c43506a68e1f23efd0ca6186a6948ae0fc8fe1e39c78cc23ef0d69f3569d")
    variant(
        "paraview", default=False, description="Build paraview plugins and runtime post-processing"
    )
    variant("vtk", default=False, description="With VTK runTimePostProcessing")
    # not know which OpenFOAM added support for 5.x and conservatively
    # use 2312 in the check.
    depends_on("flex@:2.6.1,2.6.4:")
    # Require scotch with ptscotch - corresponds to standard OpenFOAM setup
    # 1706 ok with newer paraview but avoid pv-5.2, pv-5.3 readers
    depends_on("paraview@5.4:", when="@1706:+paraview")
