from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin
from tethysdash_plugin_hydroserver.utilities import date_clamp_to_datastream, hydroserver_instance_get


class HydroServerDatastreamPlot(TethysDashPlugin):
    """HydroServer Datastream Plot Plugin"""
    
    name = "hydroserver_datastream_plot"
    args = {
        "host_url": "text",
        "api_key": "text",
        "datastream_id": "text",
        "date_start": "date",
        "date_end": "date"
    }
    group = "HydroServer"
    label = "HydroServer Datastream Plot"
    type = "plotly"
    tags = [
        "hydroserver",
        "plotly",
        "datastream",
    ]
    description = "A plugin for visualizing a datastream from a HydroServer using Plotly"
    restricted = True

    def run(self):
        """
        Fetch data from a HydroServer datastream and return it in a format suitable for Plotly plotting
        """
        # Get the HydroServer API instance
        hs_api = hydroserver_instance_get(self.host_url, self.api_key)
        
        # Get the datastream object from the HydroServer API
        datastream = hs_api.datastreams.get(uid=self.datastream_id)
        
        # Determine the start and end dates for the observation query
        date_start = date_clamp_to_datastream(self.get_arg("date_start"), datastream)
        date_end = date_clamp_to_datastream(self.get_arg("date_end"), datastream)
        
        if date_start is None:
            date_start = datastream.phenomenon_begin_time
            
        if date_end is None:
            date_end = datastream.phenomenon_end_time
        
        # Get the observations for the datastream within the specified time range
        observations = datastream.get_observations(
            phenomenon_time_min=date_start,
            phenomenon_time_max=date_end,
            fetch_all=True
        )
        
        # Convert the observations to a DataFrame for easier plotting
        df = observations.dataframe
        
        # Get the name and unit of the observed property for the y-axis
        observed_property = None
        unit = None
        y_axis_observed_property_name = "Unknown"
        y_axis_unit_symbol = "Unknown"
        
        try:
            # Attempt to get the observed property and unit from the datastream
            observed_property = datastream.observed_property
            unit = datastream.unit
            
            # Get the name and symbol for the y-axis labels
            y_axis_observed_property_name = observed_property.name
            y_axis_unit_symbol = unit.symbol
        except Exception:
            pass
        
        if df.empty:
            return {
                "data": [],
                "layout": {
                    "title": datastream.name,
                    "xaxis": {"title": "Date"},
                    "yaxis": {"title": "No Data"},
                },
            }
        
        # Return the plotly data and layout for the datastream observations
        return {
            "data": [
                {
                    "x": df["phenomenon_time"].tolist(),
                    "y": df["result"].tolist(),
                    "type": "scatter",
                    "mode": "lines+markers",
                }
            ],
            "layout": {
                "title": datastream.name,
                "xaxis": {"title": "Date"},
                "yaxis": {"title": f"{y_axis_observed_property_name} ({y_axis_unit_symbol})"},
            },
        }
