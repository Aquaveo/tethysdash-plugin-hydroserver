from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin, LayerConfigurationBuilder
from tethysdash_plugin_hydroserver.utilities import hydroserver_instance_get, hydroserver_workspace_sites_geojson_get
from tethysdash_plugin_hydroserver.symbology import sites_symbology_build


class HydroServerSitesMapLayer(TethysDashPlugin):
    """HydroServer Sites Map Layer Plugin"""
    name = "hydroserver_sites_map_layer"
    args = {
        "host_url": "text",
        "api_key": "text",
        "workspace_id": "text",
    }
    group = "HydroServer"
    label = "HydroServer Sites Map Layer"
    type = "map_layer"
    tags = [
        "hydroserver",
        "openlayers",
        "sites",
        "map layer",
    ]
    description = "A plugin for adding a HydroServer sites map layer to a map"
    dynamic_map_layer = True
    dynamic_map_layer_source = "GeoJSON"
    restricted = True

    LAYER_NAME = "HydroServer Sites"

    def run(self):
        """
        Build the configure-time scaffold for the sites map layer.

        Returns:
            dict: A dynamic map-layer configuration whose features are supplied
                at render time by fetch_features().
        """
        # Get the arguments for the HydroServer connection
        host_url = self.get_arg("host_url")
        api_key = self.get_arg("api_key")
        workspace_id = self.get_arg("workspace_id")

        # Configure the layer for displaying the sites on the map
        layer_builder = LayerConfigurationBuilder(self.LAYER_NAME, "GeoJSON")
        layer_builder.set_plugin_source("hydroserver_sites_map_layer", {
            "host_url": host_url,
            "api_key": api_key,
            "workspace_id": workspace_id,
        })

        # Give the raw property keys human-readable labels in the popup
        layer_builder.add_attribute_alias("name", "Site Name", self.LAYER_NAME)
        layer_builder.add_attribute_alias("code", "Site Code", self.LAYER_NAME)
        layer_builder.add_attribute_alias("site_type", "Site Type", self.LAYER_NAME)
        layer_builder.add_attribute_alias("description", "Description", self.LAYER_NAME)
        layer_builder.add_attribute_alias("elevation", "Elevation", self.LAYER_NAME)
        layer_builder.add_attribute_alias("location", "Location", self.LAYER_NAME)

        # Set the hydroserver_site_id attribute variable to the clicked site's id so other dashboard components can react to the selection
        layer_builder.add_attribute_variable("id", "hydroserver_site_id", self.LAYER_NAME)

        # The id is only needed for the attribute variable, so hide it from the popup
        layer_builder.omit_popup_attribute("id", self.LAYER_NAME)

        # Only attempt to fetch and style the sites if all connection parameters are provided
        if host_url and api_key and workspace_id:
            # Get the HydroServer API instance
            hs_api = hydroserver_instance_get(host_url, api_key)

            # Fetch the GeoJSON feature collection for the workspace's sites
            feature_collection = hydroserver_workspace_sites_geojson_get(hs_api, workspace_id)

            # Build the symbology for the sites based on the feature collection
            style, legend = sites_symbology_build(feature_collection)

            # Apply the style and legend to the layer configuration
            layer_builder.set_style(style)
            layer_builder.set_legend(legend)

        # Return the final layer configuration
        return layer_builder.build()

    def fetch_features(self):
        """
        Fetch the workspace's sites for the map to render.

        Returns:
            dict: A GeoJSON FeatureCollection of the workspace's sites.
        """
        # Get the HydroServer API instance
        hs_api = hydroserver_instance_get(self.host_url, self.api_key)

        # Fetch the GeoJSON feature collection for the workspace's sites
        return hydroserver_workspace_sites_geojson_get(hs_api, self.workspace_id)
