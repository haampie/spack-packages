from spack.package import *
class Openfoam(Package):
    version("2306", sha256="d7fba773658c0f06ad17f90199565f32e9bf502b7bb03077503642064e1f5344")
    variant(
        "paraview", default=False, description="Build paraview plugins and runtime post-processing"
    )
    depends_on("flex@:2.6.1,2.6.4:")
    depends_on("cmake", type="build")
    depends_on("paraview@5.4:", when="@1706:+paraview")
