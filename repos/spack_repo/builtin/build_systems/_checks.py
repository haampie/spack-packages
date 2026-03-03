from typing import List
from spack.package import (
    Builder,
    Spec,
)
def ensure_build_dependencies_or_raise(spec: Spec, dependencies: List[str], error_msg: str):
    msg = (
    )
    for dep in missing_deps:
        msg += '    depends_on("{0}", type="build", when="@{1} {2}")\n'.format(
        )
def execute_build_time_tests(builder: Builder):
    """Execute the build-time tests prescribed by builder.
    """
