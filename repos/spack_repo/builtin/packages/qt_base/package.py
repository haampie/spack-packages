from spack_repo.builtin.build_systems.cmake import CMakePackage, generator
class QtPackage(CMakePackage):
        _list_url = "https://github.com/qt/{}/tags"
class QtBase(QtPackage):
    """Qt Base (Core, Gui, Widgets, Network, ...)"""
