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

from typing import Union

import click

import dg.config

from dg.utils.logging import loglevel_command


@loglevel_command()
@click.option("--artifactory-api-key", help="Artifactory API key")
@click.option("--artifactory-user-name", help="Artifactory user name")
@click.option("--ibm-cloud-api-key", help="IBM Cloud API key")
@click.option(
    "--ibm-cloud-pak-for-data-entitlement-key",
    help="IBM Cloud Pak for Data entitlement key",
)
@click.option("--ibm-github-api-key", help="IBM GitHub API key")
def store_credentials(
    artifactory_api_key: Union[str, None],
    artifactory_user_name: Union[str, None],
    ibm_cloud_api_key: Union[str, None],
    ibm_cloud_pak_for_data_entitlement_key: Union[str, None],
    ibm_github_api_key: Union[str, None],
):
    """Store credentials in a configuration file"""

    credentials_to_be_stored = locals().copy()

    dg.config.data_gate_configuration_manager.store_credentials(credentials_to_be_stored)
