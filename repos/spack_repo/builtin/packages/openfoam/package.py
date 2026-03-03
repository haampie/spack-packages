import glob
import os
import re
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
    homepage = "https://www.openfoam.com/"
    url = "https://sourceforge.net/projects/openfoam/files/v1906/OpenFOAM-v1906.tgz"
    git = "https://gitlab.com/openfoam/core/openfoam.git"
    list_url = "https://sourceforge.net/projects/openfoam/files/"
    list_depth = 2
    version("develop", branch="develop", submodules=True)
    variant("mgridgen", default=False, description="With mgridgen support")
    variant(
        "paraview", default=False, description="Build paraview plugins and runtime post-processing"
    )
    variant("vtk", default=False, description="With VTK runTimePostProcessing")
    # After 1712, could suggest openmpi+thread_multiple for collated output
    # conflicts('^openmpi~thread_multiple', when='@1712:')
    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # Earlier versions of OpenFOAM may not work with CGAL 5.6. I do
    # not know which OpenFOAM added support for 5.x and conservatively
    # use 2312 in the check.
    # cgal@6 needs c++17, but until v2412 OpenFOAM forced c++14
    depends_on("cgal@:4", when="@:2306")
    # The flex restriction is ONLY to deal with a spec resolution clash
    # introduced by the restriction within scotch!
    depends_on("flex@:2.6.1,2.6.4:")
    # mgridgen is statically linked
    # 'paraview+plugins' but that resolves poorly.
    # 1612 plugins need older paraview
    depends_on("paraview@:5.0.1", when="@1612+paraview")
    # Icx only support from v2106 onwards
    # General patches
    assets = []  # type: List[str]
    # Version-specific patches
    # kahip patch (wmake)
    phases = ["configure", "build", "install"]
    build_script = "./spack-Allwmake"  # From patch() method.
    #
