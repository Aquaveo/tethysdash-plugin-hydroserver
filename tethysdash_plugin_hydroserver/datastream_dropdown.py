from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin
from tethysdash_plugin_hydroserver.utilities import hydroserver_instance_get


class HydroServerDatastreamDropdown(TethysDashPlugin):
    """HydroServer Datastream Dropdown Plugin"""
    name = "hydroserver_datastream_dropdown"
    args = {
        "host_url": "text",
        "api_key": "text",
        "workspace_id": "text",
        "site_id": "text",          # Optional
    }
    group = "HydroServer"
    label = "HydroServer Datastream Dropdown"
    type = "variable_input"
    tags = [
        "hydroserver",
        "variable input",
        "datastream",
    ]
    description = "A plugin for selecting a datastream from a HydroServer workspace using a dropdown menu"
    restricted = True

    VARIABLE_NAME = "HydroServer Datastream"

    def run(self):
        """Build the configure-time scaffold for the datastream dropdown.

        Returns:
            dict: A configuration for the datastream dropdown variable input.
        """
        # Get the arguments
        host_url = self.get_arg("host_url")
        api_key = self.get_arg("api_key")
        workspace_id = self.get_arg("workspace_id")
        site_id = self.get_arg("site_id")

        # Return an empty dropdown if any of the required arguments are missing
        if not host_url or not api_key or not workspace_id:
            return {
                "variable_name": self.VARIABLE_NAME,
                "initial_value": "",
                "variable_options_source": "dropdown",
                "metadata": {
                    "choices": []
                }
            }

        # Get the HydroServer API instance
        hs_api = hydroserver_instance_get(host_url, api_key)

        # Fetch the list of datastreams for the workspace
        if site_id:
            datastreams = hs_api.datastreams.list(workspace=workspace_id, thing=site_id, fetch_all=True)
        else:
            datastreams = hs_api.datastreams.list(workspace=workspace_id, fetch_all=True)

        # Fetch and map each site's id to its name so datastreams can be labeled by their site
        sites = hs_api.things.list(workspace=workspace_id, fetch_all=True)
        sites_name_id_map = {str(site.uid): site.name for site in sites.items}

        # Initialize the choices list for the dropdown
        choices = []
        for datastream in datastreams.items:
            # Get the site name for the datastream's associated site
            site_name = sites_name_id_map.get(str(datastream.thing_id), "Unknown Site")

            # Append the datastream to the list of choices for the dropdown
            choices.append({
                "value": str(datastream.uid),
                "label": f"{site_name} - ({datastream.name})"
            })

        # Sort the choices alphabetically by label
        choices.sort(key=lambda x: x["label"])

        # Return the dropdown configuration
        return {
            "variable_name": self.VARIABLE_NAME,
            "initial_value": "",
            "variable_options_source": "dropdown",
            "metadata": {
                "choices": choices
            }
        }
