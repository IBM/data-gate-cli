import json

from typing import Any, Union

import semver

from dg.lib.cloud_pak_for_data.cpd_manager import (
    AbstractCloudPakForDataManager,
)
from dg.lib.error import DataGateCLIException
from dg.lib.ibmcloud import execute_ibmcloud_command


def get_latest_supported_openshift_version() -> str:
    current_openshift_version: Union[semver.VersionInfo, None] = None
    ibm_cloud_supported_cloud_pak_for_data_version = AbstractCloudPakForDataManager.get_ibm_cloud_supported_version()
    version_command_result_json = _get_oc_versions_as_json()

    if version_command_result_json and "openshift" in version_command_result_json:
        for version in version_command_result_json["openshift"]:
            major = version["major"]
            minor = version["minor"]
            patch = version["patch"]
            openshift_version = semver.VersionInfo.parse(f"{major}.{minor}.{patch}")

            if AbstractCloudPakForDataManager.is_openshift_version_supported(
                ibm_cloud_supported_cloud_pak_for_data_version, openshift_version
            ):
                if (current_openshift_version is None) or (openshift_version.compare(current_openshift_version) == 1):
                    current_openshift_version = openshift_version

    if current_openshift_version is None:
        raise DataGateCLIException(
            f"None of the OpenShift versions available in IBM Cloud is supported by IBM Cloud Pak for Data "
            f"{str(ibm_cloud_supported_cloud_pak_for_data_version)}:\n{version_command_result_json}"
        )
    else:
        full_openshift_version = f"{str(current_openshift_version)}_openshift"

        return full_openshift_version


def _get_oc_versions_as_json() -> Any:
    args = ["oc", "versions", "--json"]
    version_command_result = execute_ibmcloud_command(args, capture_output=True)
    version_command_result_json = json.loads(version_command_result.stdout)

    return version_command_result_json
