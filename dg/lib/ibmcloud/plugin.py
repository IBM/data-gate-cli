import click

from dg.utils.thirdparty import execute_ibmcloud_command_with_check


def install_catalogs_management_plugin():
    _install_plugin("catalogs-management")


def install_container_service_plugin():
    _install_plugin("container-service")


def is_catalogs_management_plugin_installed() -> bool:
    return _is_plugin_installed("catalogs-management")


def is_container_service_plugin_installed() -> bool:
    return _is_plugin_installed("container-service")


def _install_plugin(plugin_name: str):
    click.echo(f"Installing IBM Cloud plug-in '{plugin_name}'")

    args = ["plugin", "install", plugin_name]
    result = execute_ibmcloud_command_with_check(args)

    if result.returncode != 0:
        raise Exception(
            f"An error occurred when attempting to install ibmcloud plug-in {plugin_name}:\n{result.stderr}"
        )


def _is_plugin_installed(plugin_name: str) -> bool:
    args = ["plugin", "list"]
    result = execute_ibmcloud_command_with_check(args)

    if result.returncode != 0:
        raise Exception(
            f"An error occurred when attempting to check whether ibmcloud plug-in {plugin_name} is installed:\n"
            f"{result.stderr}"
        )

    is_installed = plugin_name in result.stdout

    return is_installed