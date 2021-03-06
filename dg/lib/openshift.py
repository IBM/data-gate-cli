#  Copyright 2020 IBM Corporation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import json
import urllib.parse

from typing import Final, List

import requests
import semver

import dg.config
import dg.utils.network
import dg.utils.process

from dg.lib.error import DataGateCLIException

OPENSHIFT_REST_API_VERSION: Final[str] = "v1"


def enable_openshift_image_registry_default_route():
    """Enables the Image Registry default route with the Custom Resource
    Definition

    https://docs.openshift.com/container-platform/latest/registry/configuring-registry-operator.html#registry-operator-default-crd_configuring-registry-operator
    """

    oc_patch_args = [
        "patch",
        "configs.imageregistry.operator.openshift.io/cluster",
        "--patch",
        '{"spec":{"defaultRoute":true}}',
        "--type",
        "merge",
    ]

    execute_oc_command(oc_patch_args)


def execute_oc_command(
    args: list[str],
    capture_output=False,
    check=True,
    oc_cli_path=dg.config.data_gate_configuration_manager.get_oc_cli_path(),
    print_captured_output=False,
) -> dg.utils.process.ProcessResult:
    """Executes the OpenShift Container Platform CLI

    Parameters
    ----------
    args
        arguments to be passed to the OpenShift Container Platform CLI
    capture_output
        flag indicating whether output shall be captured
    check
        flag indicating whether an exception shall be thrown if the OpenShift
        Container Platform CLI returns with a nonzero return code
    oc_cli_path
        path to the OpenShift Container Platform CLI
    print_captured_output
        flag indicating whether captured output shall also be written to
        stdout/stderr

    Returns
    -------
    ProcessResult
        object storing the return code and captured output (if requested)
    """

    return dg.utils.process.execute_command(
        oc_cli_path,
        args,
        capture_output=capture_output,
        check=check,
        print_captured_output=print_captured_output,
    )


def get_cluster_access_token(oauth_server_url: str, username: str, password: str) -> str:
    """Obtains an OAuth access token from the given OpenShift server

    Parameters
    ----------
    oauth_server_url
        URL of the OpenShift server that the OAuth access token shall be
        obtained from
    username
        username used to authenticate with the OpenShift server
    password
        password used to authenticate with the OpenShift server

    Returns
    -------
    str
        OAuth access token obtained from the given OpenShift server
    """

    dg.utils.network.disable_insecure_request_warning()

    response = requests.get(
        oauth_server_url,
        allow_redirects=False,
        auth=(username, password),
        verify=False,
    )

    if "Location" not in response.headers:
        raise DataGateCLIException("HTTP Location header not found")

    fragment = urllib.parse.parse_qs(urllib.parse.urlparse(response.headers["Location"]).fragment)

    if "access_token" not in fragment:
        raise DataGateCLIException("access_token key not found in URL fragment")

    access_token = fragment["access_token"][0]

    return access_token


def get_current_token() -> str:
    """Returns the current OAuth access token stored in ~/.kube/config

    Returns
    -------
    str
        current OAuth access token stored in ~/.kube/config
    """

    oc_whoami_args = [
        "whoami",
        "--show-token",
    ]

    oc_whoami_command_result = execute_oc_command(oc_whoami_args, capture_output=True)

    return oc_whoami_command_result.stdout.rstrip()


def get_oc_login_args_with_password(server: str, username: str, password: str) -> List[str]:
    return [
        "login",
        "--insecure-skip-tls-verify",
        "--password",
        password,
        "--server",
        server,
        "--username",
        username,
    ]


def get_oc_login_args_with_token(server: str, token: str) -> List[str]:
    return [
        "login",
        "--insecure-skip-tls-verify",
        "--server",
        server,
        "--token",
        token,
    ]


def get_oc_login_command_with_password_for_remote_host(server: str, username: str, password: str) -> str:
    return " ".join(["oc"] + get_oc_login_args_with_password(server, username, password))


def get_oc_login_command_with_token_for_remote_host(server: str, token: str) -> str:
    return " ".join(["oc"] + get_oc_login_args_with_token(server, token))


def get_openshift_image_registry_default_route() -> str:
    """Returns the Image Registry default route

    Returns
    -------
    str
        Image Registry default route
    """

    oc_get_route_args = [
        "get",
        "route",
        "--namespace",
        "openshift-image-registry",
        "--output",
        "jsonpath='{.items[?(@.metadata.name==\"default-route\")].spec.host}'",
    ]

    oc_get_route_command_result = (
        execute_oc_command(oc_get_route_args, capture_output=True).stdout.removeprefix("'").removesuffix("'")
    )

    return oc_get_route_command_result


def get_openshift_version() -> semver.VersionInfo:
    oc_version_args = ["version", "--output", "json"]
    oc_version_command_result = json.loads(execute_oc_command(oc_version_args, capture_output=True).stdout)

    return semver.VersionInfo.parse(oc_version_command_result["openshiftVersion"])


def get_persistent_volume_name(namespace: str, persistent_volume_claim_name: str) -> str:
    oc_get_pvc_args = [
        "get",
        "pvc",
        "--namespace",
        namespace,
        "--output",
        "json",
    ]

    oc_get_pvc_command_result = json.loads(execute_oc_command(oc_get_pvc_args, capture_output=True).stdout)

    if len(oc_get_pvc_command_result["items"]) == 0:
        raise DataGateCLIException(
            f"Namespace '{namespace}' does not contain a persistent volume claim with name "
            f"'{persistent_volume_claim_name}''"
        )

    volumeName = oc_get_pvc_command_result["items"][0]["spec"]["volumeName"]

    return volumeName


def get_persistent_volume_id(namespace: str, persistent_volume_name: str):
    oc_get_pv_args = [
        "get",
        "pv",
        "--output",
        f"jsonpath='{{.items[?(@.metadata.name==\"{persistent_volume_name}\")].metadata.labels.volumeId}}'",
    ]

    oc_get_pv_command_result = (
        execute_oc_command(oc_get_pv_args, capture_output=True).stdout.removeprefix("'").removesuffix("'")
    )

    if oc_get_pv_command_result == "":
        raise DataGateCLIException(f"Persistent volume with name '{persistent_volume_name}' could not be found")

    return oc_get_pv_command_result


def log_in_to_openshift_cluster_with_password(server: str, username: str, password: str):
    """Logs in to a given Openshift cluster with the given credentials"""

    oc_login_args = get_oc_login_args_with_password(server, username, password)

    execute_oc_command(oc_login_args)


def log_in_to_openshift_cluster_with_token(server: str, token: str):
    """Logs in to a given Openshift cluster with the given OAuth access
    token"""

    oc_login_args = get_oc_login_args_with_token(server, token)

    execute_oc_command(oc_login_args)
