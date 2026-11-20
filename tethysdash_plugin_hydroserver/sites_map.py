from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin, LayerConfigurationBuilder
from tethysdash_plugin_hydroserver.utilities import (
    hydroserver_instance_get,
    hydroserver_workspace_sites_geojson_get,
)
from tethysdash_plugin_hydroserver.symbology import sites_symbology_build


class HydroServerSitesMap(TethysDashPlugin):
    """HydroServer Sites Map Plugin"""
    name = "hydroserver_sites_map"
    args = {
        "host_url": "text",
        "api_key": "text",
        "workspace_id": "text",
    }
    group = "HydroServer"
    label = "HydroServer Sites Map"
    type = "map"
    tags = [
        "hydroserver",
        "openlayers",
        "sites",
        "map",
    ]
    description = "A plugin for visualizing HydroServer sites on a map"
    restricted = True
    
    LAYER_NAME = "HydroServer Sites"

    def run(self):
        """
        Fetch the sites for the configured workspace and return a map visualization of them as a GeoJSON point layer.
        """
        # Get the HydroServer API instance
        hs_api = hydroserver_instance_get(self.host_url, self.api_key)

        # Fetch the workspace's sites as a GeoJSON FeatureCollection
        geojson_sites_feature_collection = hydroserver_workspace_sites_geojson_get(hs_api, self.workspace_id)

        # Build the curated-with-fallback symbology and matching legend from the sites
        sites_style, sites_legend = sites_symbology_build(geojson_sites_feature_collection)

        # Configure the layer for displaying the sites on the map
        layer_builder = LayerConfigurationBuilder(self.LAYER_NAME, "GeoJSON")
        layer_builder.set_geojson(geojson_sites_feature_collection)
        layer_builder.set_style(sites_style)
        layer_builder.set_legend(sites_legend)

        # Give the raw property keys human-readable labels in the popup
        layer_builder.add_attribute_alias("name", "Site Name", self.LAYER_NAME)
        layer_builder.add_attribute_alias("code", "Site Code", self.LAYER_NAME)
        layer_builder.add_attribute_alias("site_type", "Site Type", self.LAYER_NAME)
        layer_builder.add_attribute_alias("description", "Description", self.LAYER_NAME)
        layer_builder.add_attribute_alias("elevation", "Elevation", self.LAYER_NAME)
        layer_builder.add_attribute_alias("location", "Location", self.LAYER_NAME)

        # Set the "HydroServer Site" attribute variable to the clicked site's id so other dashboard components can react to the selection
        layer_builder.add_attribute_variable("id", "HydroServer Site", self.LAYER_NAME)

        # The id is only needed for the attribute variable, so hide it from the popup
        layer_builder.omit_popup_attribute("id", self.LAYER_NAME)

        # Build the final layer configuration for the sites
        sites_layer = layer_builder.build()

        # Return the map configuration with the base map and the sites layer
        return {
            "baseMap": "https://server.arcgisonline.com/arcgis/rest/services/Canvas/World_Light_Gray_Base/MapServer",
            "layers": [sites_layer],
            "layerControl": True
        }