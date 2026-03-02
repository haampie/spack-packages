# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.oneapi import (
    IntelOneApiLibraryPackageWithSdk,
    IntelOneApiPackage,
)

from spack.package import *


@IntelOneApiPackage.update_description
class IntelOneapiVtune(IntelOneApiLibraryPackageWithSdk):
    """Intel VTune Profiler is a profiler to optimize application
    performance, system performance, and system configuration for HPC,
    cloud, IoT, media, storage, and more.  CPU, GPU, and FPGA: Tune
    the entire application's performance--not just the accelerated
    portion. Multilingual: Profile SYCL, C, C++, C#, Fortran, OpenCL
    code, Python, Google Go programming language, Java, .NET,
    Assembly, or any combination of languages.  System or Application:
    Get coarse-grained system data for an extended period or detailed
    results mapped to source code. Power: Optimize performance while
    avoiding power and thermal-related throttling.

    """

    maintainers("rscohn2")

    homepage = "https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/vtune-profiler.html"

    version(
        "2025.8.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/8ab935f9-98cd-46b2-8e3f-df29ef73af84/intel-vtune-2025.8.1.8_offline.sh",
        sha256="bf47be3140f89b7e85eb09aad1314d032621e4a8c2fa4e0dab934a3c349e4a5e",
        expand=False,
    )
    version(
        "2025.8.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/15ddff8e-7875-4973-9120-fa2e18759fba/intel-vtune-2025.8.0.9_offline.sh",
        sha256="d35cd3a7220d0156b64fcee468a04649de4be50ba14a04232bc411c6226f941b",
        expand=False,
    )
    version(
        "2025.7.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/a04c89ad-d663-4f70-bd3d-bb44f5c16d57/intel-vtune-2025.7.0.248_offline.sh",
        sha256="4bc06c56eab368ee0ff57e87ea0f563663db6c60ea3f9cf9badf16928e43e321",
        expand=False,
    )
    version(
        "2025.6.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/a62585a0-db22-4fc3-8554-a5ed74d5a4e8/intel-vtune-2025.6.0.31_offline.sh",
        sha256="60830610ce9807f951285c89f585f001c339a8c6deaa4bc8db33931ba7ae6167",
        expand=False,
    )
    version(
        "2025.1.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/05b14253-a457-4472-bcf7-d98676542072/intel-vtune-2025.1.0.686_offline.sh",
        sha256="26407e12d501e544431535da5e9f3ea2ac56c9c53660b410c3096f2b9aae2a89",
        expand=False,
    )
    version(
        "2025.0.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/1277cea4-34b7-4221-bdbc-4f47a9a5592d/intel-vtune-2025.0.1.16_offline.sh",
        sha256="e0917aab901018d2786df2fcfbaea2bf9c4ff7d5b7f9413e9f3d6860bb743f82",
        expand=False,
    )
    version(
        "2025.0.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/e7797b12-ce87-4df0-aa09-df4a272fc5d9/intel-vtune-2025.0.0.1130_offline.sh",
        sha256="6742e5c6b1cd6e4efb794bde5d995ba738be1a991ac84678e0efca04fc080074",
        expand=False,
    )
    version(
        "2024.0.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/56d0db2b-1ff1-4abe-857a-72ca9be22bd3/l_oneapi_vtune_p_2024.0.1.14_offline.sh",
        sha256="2c9b28ed91562deeea211b341cb257cc55051ac29c064b9cf65b4517b958724d",
        expand=False,
    )
    version(
        "2022.4.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/19027/l_oneapi_vtune_p_2022.4.1.16919_offline.sh",
        sha256="eb4b4da61eea52c08fc139dbf4630e2c52cbcfaea8f1376c545c0863839366d1",
        expand=False,
    )
    version(
        "2022.4.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18888/l_oneapi_vtune_p_2022.4.0.8705_offline.sh",
        sha256="8c5a144ed61ef9addaa41abe7fbfceeedb6a8fe1c5392e3e265aada1f545b0fe",
        expand=False,
    )
    version(
        "2022.3.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18656/l_oneapi_vtune_p_2022.3.0.195_offline.sh",
        sha256="7921fce7fcc3b82575be22d9c36beec961ba2a9fb5262ba16a04090bcbd2e1a6",
        expand=False,
    )
    version(
        "2022.0.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18406/l_oneapi_vtune_p_2022.0.0.94_offline.sh",
        sha256="aa4d575c22e7be0c950b87d67d9e371f470f682906864c4f9b68e530ecd22bd7",
        expand=False,
    )
    version(
        "2021.7.1",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18086/l_oneapi_vtune_p_2021.7.1.492_offline.sh",
        sha256="4cf17078ae6e09f26f70bd9d0b726af234cc30c342ae4a8fda69941b40139b26",
        expand=False,
    )
    version(
        "2021.6.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/18012/l_oneapi_vtune_p_2021.6.0.411_offline.sh",
        sha256="6b1df7da713337aa665bcc6ff23e4a006695b5bfaf71dffd305cbadca2e5560c",
        expand=False,
    )

    @property
    def v2_layout_versions(self):
        return "@2024:"

    @property
    def component_dir(self):
        return "vtune"
