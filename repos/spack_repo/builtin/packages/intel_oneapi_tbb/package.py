# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.oneapi import IntelOneApiLibraryPackage, IntelOneApiPackage

from spack.package import *


@IntelOneApiPackage.update_description
class IntelOneapiTbb(IntelOneApiLibraryPackage):
    """Intel oneAPI Threading Building Blocks (oneTBB) is a flexible
    performance library that simplifies the work of adding
    parallelism to complex applications across accelerated
    architectures, even if you are not a threading expert.

    """

    maintainers("rscohn2")

    homepage = (
        "https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/onetbb.html"
    )

    version(
        "2022.3.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/233a8b7a-ec95-4e51-bc5f-9dcd4f0d1dc3/intel-onetbb-2022.3.1.402_offline.sh",
        sha256="cbd986db85a6f8b2d924ef00bf9a8ac2f781690e64611cccdb60eb18bb658d3b",
        expand=False,
    )
    version(
        "2022.3.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/1134c0a9-1960-465a-ac29-3b692e45f417/intel-onetbb-2022.3.0.383_offline.sh",
        sha256="a65ce842b88b1bbb1bec57649932b2eaa7eb008667a6086d80b982a7b80bac50",
        expand=False,
    )
    version(
        "2022.2.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/7516db94-4877-4ffe-8dde-37e9a46e69a2/intel-onetbb-2022.2.0.508_offline.sh",
        sha256="b8da6678bf4fdd4bf780436c21d191fe13a5ec71db21c8af9e10e3c6209d258e",
        expand=False,
    )
    version(
        "2021.12.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/b31f6b79-10aa-4119-a437-48fe2775633b/l_tbb_oneapi_p_2021.12.0.499_offline.sh",
        sha256="13e981cb4d9d3f72058cc136f8cdedf6ba9af225ae317f91b59e2050b0d49e43",
        expand=False,
    )
    version(
        "2021.11.0",
        url="https://registrationcenter-download.intel.com/akdlm//IRC_NAS/af3ad519-4c87-4534-87cb-5c7bda12754e/l_tbb_oneapi_p_2021.11.0.49527_offline.sh",
        sha256="dd878ee979d7b6da4eb973adfebf814d9d7eed86b875d31e3662d100b2fa0956",
        expand=False,
    )
    version(
        "2021.10.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/c95cd995-586b-4688-b7e8-2d4485a1b5bf/l_tbb_oneapi_p_2021.10.0.49543_offline.sh",
        sha256="a10d319e67b6904d6199f8294e970124a064d9948cf7e2b5ebab94499aadc6ca",
        expand=False,
    )
    version(
        "2021.9.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/7dcd261b-12fa-418a-b61b-b3dd4d597466/l_tbb_oneapi_p_2021.9.0.43484_offline.sh",
        sha256="77f7a256e0035d2d7b911a4b8b398f293991c7c8705ef6c94d48f4cfd760018d",
        expand=False,
    )
    version(
        "2021.5.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18473/l_tbb_oneapi_p_2021.5.1.738_offline.sh",
        sha256="c154749f1f370e4cde11a0a7c80452d479e2dfa53ff2b1b97003d9c0d99c91e3",
        expand=False,
    )
    version(
        "2021.5.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18380/l_tbb_oneapi_p_2021.5.0.707_offline.sh",
        sha256="6ff7890a74a43ae02e0fa2d9c5533fce70a49dff8e73278b546a0995367fec5e",
        expand=False,
    )
    version(
        "2021.4.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18194/l_tbb_oneapi_p_2021.4.0.643_offline.sh",
        sha256="33332012ff8ffe7987b1a20bea794d76f7d8050ccff04fa6e1990974c336ee24",
        expand=False,
    )
    version(
        "2021.3.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/17952/l_tbb_oneapi_p_2021.3.0.511_offline.sh",
        sha256="b83f5e018e3d262e42e9c96881845bbc09c3f036c265e65023422ca8e8637633",
        expand=False,
    )
    version(
        "2021.2.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/17759/l_tbb_oneapi_p_2021.2.0.357_offline.sh",
        sha256="c1c3623c5bef547b30eac009e7a444611bf714c758d7472c114e9be9d5700eba",
        expand=False,
    )
    version(
        "2021.1.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/17378/l_tbb_oneapi_p_2021.1.1.119_offline.sh",
        sha256="535290e3910a9d906a730b24af212afa231523cf13a668d480bade5f2a01b53b",
        expand=False,
    )

    provides("tbb")

    @property
    def component_dir(self):
        return "tbb"

    @property
    def v2_layout_versions(self):
        return "@2021.11:"

    @run_after("install")
    def fixup_prefix(self):
        # The motivation was to provide a more standard layout so tbb
        # would be more likely to work as a virtual dependence. I am
        # not sure if this mechanism is useful and it became a problem
        # for mpi so disabling for v2_layout.
        if self.v2_layout:
            return
        self.symlink_dir(self.component_prefix.include, self.prefix.include)
        self.symlink_dir(self.component_prefix.lib, self.prefix.lib)
