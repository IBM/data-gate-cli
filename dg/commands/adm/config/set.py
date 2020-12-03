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

import click

import dg.config


@click.command()
@click.option(
    "--key",
    required=True,
    help="Key name which should be set",
)
@click.option(
    "--value",
    required=True,
    help="Value to which key should be set",
)
def set(key: str, value: str):
    """Set configuration value"""

    bool_value = False
    if value.lower() in ("true", "yes", "enable"):
        bool_value = True
    elif value.lower() in ("false", "no", "disable"):
        bool_value = False
    else:
        raise Exception("Only boolean values are supported at the moment")

    dg.config.data_gate_configuration_manager.set_dg_bool_config_value(key, bool_value)
