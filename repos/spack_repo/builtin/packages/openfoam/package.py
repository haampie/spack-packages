from spack.package import *
__all__ = [
]
class Openfoam(Package):
    version("2212", sha256="0a3ddbfea9abca04c3a811e72fcbb184c6b1f92c295461e63b231f1a97e96476")
    variant(
        "paraview", default=False, description="Build paraview plugins and runtime post-processing"
    )
    depends_on("flex@:2.6.1,2.6.4:")
    depends_on("json-c")
    depends_on("paraview@5.4:", when="@1706:+paraview")
