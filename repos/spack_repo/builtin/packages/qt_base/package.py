from spack_repo.builtin.build_systems.cmake import CMakePackage, generator
class QtPackage(CMakePackage):
    def get_url(qualname):
        return _list_url.format(qualname.lower())
class QtBase(QtPackage):
    """Qt Base (Core, Gui, Widgets, Network, ...)"""
