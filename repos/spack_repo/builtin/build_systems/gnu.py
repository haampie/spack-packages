from typing import Optional
from spack.package import PackageBase, join_url
class GNUMirrorPackage(PackageBase):
    gnu_mirror_path: Optional[str] = None
