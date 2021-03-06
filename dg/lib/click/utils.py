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
import pathlib

from typing import Any

import click

import dg.config.cluster_credentials_manager
import dg.lib.openshift

from dg.lib.cloud_pak_for_data.cpd_manager import (
    CloudPakForDataAssemblyBuildType,
)


def check_cloud_pak_for_data_options(
    ctx: click.Context,
    build_type: CloudPakForDataAssemblyBuildType,
    options: dict[str, Any],
):
    """Checks if values for required Click options were passed to a Click
    command to install an IBM Cloud Pak for Data assembly

    Parameters
    ----------
    ctx
        Click context
    build_type
        build type of an IBM Cloud Pak for Data assembly to be installed
    options
        options passed to a Click command
    """

    if build_type == CloudPakForDataAssemblyBuildType.DEV:
        if (
            ("artifactory_user_name" in options)
            and (options["artifactory_user_name"] is None)
            and ("artifactory_api_key" in options)
            and (options["artifactory_api_key"] is None)
        ):
            raise click.UsageError(
                "Missing options '--artifactory-user-name' and '--artifactory-api-key'",
                ctx,
            )
        elif ("artifactory_user_name" in options) and (options["artifactory_user_name"] is None):
            raise click.UsageError("Missing option '--artifactory-user-name'", ctx)
        elif ("artifactory_api_key" in options) and (options["artifactory_api_key"] is None):
            raise click.UsageError("Missing option '--artifactory-api-key'", ctx)
    else:
        if ("ibm_cloud_pak_for_data_entitlement_key" in options) and (
            options["ibm_cloud_pak_for_data_entitlement_key"] is None
        ):
            raise click.UsageError("Missing option '--ibm-cloud-pak-for-data-entitlement-key'", ctx)


def create_default_map_from_dict(dict: dict[str, Any]):
    default_map_dict = {}
    default_map_dict["default_map"] = dict

    return default_map_dict


def create_default_map_from_json_file(path: pathlib.Path):
    default_map_dict = {}

    if path.exists() and (path.stat().st_size != 0):
        with open(path) as json_file:
            credentials_file_contents = json.load(json_file)

            default_map_dict["default_map"] = credentials_file_contents

    return default_map_dict


def get_oc_login_command_for_remote_host(ctx: click.Context, options: dict[str, Any]) -> str:
    result: str

    if (
        ("username" in options)
        and (options["username"] is not None)
        and ("password" in options)
        and (options["password"] is not None)
    ):
        result = dg.lib.openshift.get_oc_login_command_with_password_for_remote_host(
            options["server"], options["username"], options["password"]
        )
    elif ("token" in options) and (options["token"] is not None):
        result = dg.lib.openshift.get_oc_login_command_with_token_for_remote_host(options["server"], options["token"])
    else:
        current_cluster = dg.config.cluster_credentials_manager.cluster_credentials_manager.get_current_cluster()

        if current_cluster is None:
            raise click.UsageError(
                "You must either set options '--server' and '--password', '--token', or set a current cluster.",
                ctx,
            )

        cluster_data = current_cluster.get_cluster_data()

        result = dg.lib.openshift.get_oc_login_command_with_password_for_remote_host(
            cluster_data["server"], cluster_data["username"], cluster_data["password"]
        )

    return result


def log_in_to_openshift_cluster(ctx: click.Context, options: dict[str, Any]):
    if (
        ("username" in options)
        and (options["username"] is not None)
        and ("password" in options)
        and (options["password"] is not None)
    ):
        dg.lib.openshift.log_in_to_openshift_cluster_with_password(
            options["server"], options["username"], options["password"]
        )
    elif ("token" in options) and (options["token"] is not None):
        dg.lib.openshift.log_in_to_openshift_cluster_with_token(options["server"], options["token"])
    else:
        raise click.UsageError(
            "You must either set options '--server' and '--password', '--token', or set a current cluster.",
            ctx,
        )
