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

import sys

import click

import dg.config
from dg.lib.click.lazy_loading_multi_command import create_click_multi_command_class


@click.command(
    cls=create_click_multi_command_class(sys.modules[__name__]),
    hidden=dg.config.data_gate_configuration_manager.are_nuclear_commands_hidden(),
)
def nuclear():
    """⚠ Caution - No-holds-barred administrative functions"""

    pass
