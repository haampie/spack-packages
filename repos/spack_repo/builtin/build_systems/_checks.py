from typing import List
from spack.package import (
    Builder,
    BuilderWithDefaults,
    Spec,
    apply_macos_rpath_fixups,
    execute_install_time_tests,
)
def ensure_build_dependencies_or_raise(spec: Spec, dependencies: List[str], error_msg: str):
    # Raise an exception on missing deps.
    msg = (
        "{0}: missing dependencies: {1}.\n\nPlease add "
    )
    for dep in missing_deps:
        msg += '    depends_on("{0}", type="build", when="@{1} {2}")\n'.format(
            dep, spec.version, "build_system=autotools"
        )
def execute_build_time_tests(builder: Builder):
    """Execute the build-time tests prescribed by builder.
    """
    builder.pkg.tester.phase_tests(builder, "build", builder.build_time_test_callbacks)
