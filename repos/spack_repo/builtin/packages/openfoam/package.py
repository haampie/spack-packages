from spack.package import *
# Not the nice way of doing things, but is a start for refactoring
__all__ = [
    "add_extra_files",
    "write_environ",
]
# -----------------------------------------------------------------------------
class Openfoam(Package):
    git = "https://gitlab.com/openfoam/core/openfoam.git"
    list_url = "https://sourceforge.net/projects/openfoam/files/"
    list_depth = 2
    version("develop", branch="develop", submodules=True)
    variant("mgridgen", default=False, description="With mgridgen support")
    variant(
        "paraview", default=False, description="Build paraview plugins and runtime post-processing"
    )
    variant("vtk", default=False, description="With VTK runTimePostProcessing")
    # The flex restriction is ONLY to deal with a spec resolution clash
    # introduced by the restriction within scotch!
    depends_on("flex@:2.6.1,2.6.4:")
    # mgridgen is statically linked
    # 'paraview+plugins' but that resolves poorly.
    # 1612 plugins need older paraview
    depends_on("paraview@:5.0.1", when="@1612+paraview")
    # Icx only support from v2106 onwards
    # General patches
