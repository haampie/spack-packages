import sys
from spack_repo.builtin.build_systems.cmake import CMakePackage, generator
class QtPackage(CMakePackage):
    def get_list_url(qualname):
        _list_url = "https://github.com/qt/{}/tags"
        return _list_url.format(qualname.lower())
class QtBase(QtPackage):
    """Qt Base (Core, Gui, Widgets, Network, ...)"""
