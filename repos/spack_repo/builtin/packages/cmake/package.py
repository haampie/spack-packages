from spack.package import *
class Cmake(Package):
    version("3.1.0", sha256="8bdc3fa3f2da81bc10c772a6b64cc9052acc2901d42e1e1b2588b40df224aad9")
    depends_on("cxx", type="build")
