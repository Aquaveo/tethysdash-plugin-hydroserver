from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin
from tethysdash_plugin_hydroserver.utilities import hydroserver_instance_get


class HydroServerSitesDropdown(TethysDashPlugin):
    """HydroServer Sites Dropdown Plugin"""
    name = "hydroserver_sites_dropdown"
    args = {
        "host_url": "text",
        "api_key": "text",
        "workspace_id": "text",
    }
    group = "HydroServer"
    label = "HydroServer Sites Dropdown"
    type = "variable_input"
    tags = [
        "hydroserver",
        "variable input",
        "site",
    ]
    description = "A plugin for selecting a site from a HydroServer workspace using a dropdown menu"
    restricted = True

    VARIABLE_NAME = "HydroServer Site"

    def run(self):
        """Build the configure-time scaffold for the site dropdown.

        Returns:
            dict: A configuration for the site dropdown variable input.
        """
        # Get the arguments
        host_url = self.get_arg("host_url")
        api_key = self.get_arg("api_key")
        workspace_id = self.get_arg("workspace_id")

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

        # Fetch the list of sites in the workspace
        sites = hs_api.things.list(workspace=workspace_id, fetch_all=True)

        # Initialize the choices list for the dropdown
        choices = []
        for site in sites.items:
            # Get the site name for the site
            site_name = site.name if site.name else "Unknown Site"

            # Append the site to the list of choices for the dropdown
            choices.append({
                "value": str(site.uid),
                "label": f"{site_name}"
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
