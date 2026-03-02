from typing import List
from spack.package import (
    Builder,
    BuilderWithDefaults,
    Spec,
    apply_macos_rpath_fixups,
    execute_install_time_tests,
)
# Needed to appease style checks. These names need to be exported here to be compatible
def ensure_build_dependencies_or_raise(spec: Spec, dependencies: List[str], error_msg: str):
    """Ensure that some build dependencies are present in the concrete spec.
    If not, raise a RuntimeError with a helpful error message.
    Args:
          RuntimeError: when the required build dependencies are not found
    """
def execute_build_time_tests(builder: Builder):
    """Execute the build-time tests prescribed by builder.
    Args:
        builder: builder prescribing the test callbacks. The name of the callbacks is
            stored as a list of strings in the ``build_time_test_callbacks`` attribute.
    """
