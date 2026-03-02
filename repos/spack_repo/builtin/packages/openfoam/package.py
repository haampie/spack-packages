from spack_repo.builtin.build_systems.generic import Package
from spack_repo.builtin.packages.boost.package import Boost
from spack.package import *
# Not the nice way of doing things, but is a start for refactoring
__all__ = [
    "add_extra_files",
    "write_environ",
    "rewrite_environ_files",
    "mplib_content",
    "foam_add_path",
    "foam_add_lib",
    "OpenfoamArch",
]
# -----------------------------------------------------------------------------
class Openfoam(Package):
    """OpenFOAM is a GPL-opensource C++ CFD-toolbox.
    This offering is supported by OpenCFD Ltd,
    producer and distributor of the OpenFOAM software via www.openfoam.com,
    and owner of the OPENFOAM trademark.
    OpenCFD Ltd has been developing and releasing OpenFOAM since its debut
    in 2004.
    """
    url = "https://sourceforge.net/projects/openfoam/files/v1906/OpenFOAM-v1906.tgz"
    git = "https://gitlab.com/openfoam/core/openfoam.git"
    list_url = "https://sourceforge.net/projects/openfoam/files/"
    list_depth = 2
    version("1612", sha256="2909c43506a68e1f23efd0ca6186a6948ae0fc8fe1e39c78cc23ef0d69f3569d")
    variant("scotch", default=True, description="With scotch/ptscotch decomposition")
    variant("zoltan", default=False, description="With zoltan renumbering")
    variant("mgridgen", default=False, description="With mgridgen support")
    variant(
        "paraview", default=False, description="Build paraview plugins and runtime post-processing"
    )
    variant("vtk", default=False, description="With VTK runTimePostProcessing")
    # not know which OpenFOAM added support for 5.x and conservatively
    # use 2312 in the check.
    depends_on("flex@:2.6.1,2.6.4:")
    # Require scotch with ptscotch - corresponds to standard OpenFOAM setup
    # mgridgen is statically linked
    depends_on("vtk", when="+vtk")
    # 1706 ok with newer paraview but avoid pv-5.2, pv-5.3 readers
    depends_on("paraview@5.4:", when="@1706:+paraview")
    # Icx only support from v2106 onwards
    # General patches
