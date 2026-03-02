from typing import List
from spack.package import (
    Builder,
    Spec,
)
def ensure_build_dependencies_or_raise(spec: Spec, dependencies: List[str], error_msg: str):
    """Ensure that some build dependencies are present in the concrete spec.
          RuntimeError: when the required build dependencies are not found
    """
def execute_build_time_tests(builder: Builder):
    """Execute the build-time tests prescribed by builder.
    Args:
        builder: builder prescribing the test callbacks. The name of the callbacks is
            stored as a list of strings in the ``build_time_test_callbacks`` attribute.
    """
