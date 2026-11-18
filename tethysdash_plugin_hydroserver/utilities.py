from datetime import datetime
from typing import Literal
from hydroserverpy import HydroServer
from hydroserverpy.api.models import Datastream


def hydroserver_instance_get(host_url: str, api_key: str) -> HydroServer:
    """
    Get an authenticated instance of the HydroServer client.

    Args:
        host_url (str): The URL of the HydroServer instance.
        api_key (str): The API key for authentication.

    Returns:
        HydroServer: An instance of the HydroServer client.
    """
    return HydroServer(host_url, apikey=api_key)


def hydroserver_workspace_sites_geojson_get(hs_api: HydroServer, workspace_id: str) -> dict:
    """
    Get a GeoJSON FeatureCollection for the sites in the specified workspace.

    Args:
        hs_api (HydroServer): An authenticated HydroServer instance.
        workspace_id (str): The ID of the workspace containing the sites.

    Returns:
        dict: A GeoJSON FeatureCollection representing the sites.
    """
    # Fetch all sites from the specified workspace using the HydroServer API
    sites = hs_api.things.list(workspace=workspace_id, fetch_all=True)

    # Build a GeoJSON FeatureCollection for the sites
    geojson_site_feature_collection = {
        "type": "FeatureCollection",
        "crs": {
            "type": "name",
            "properties": {
                "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
            }
        },
        "features": []
    }

    # Convert each site into a GeoJSON feature and add it to the FeatureCollection
    for site in sites.items:
        # Add the basic properties for the site
        properties = {
            "id": str(site.uid),
            "name": site.name,
            "code": site.sampling_feature_code,
            "site_type": site.site_type,
        }

        # Add the description property if it exists
        if site.description:
            properties["description"] = site.description

        # Add the elevation property if it exists
        if site.elevation_m is not None:
            if site.elevation_datum:
                properties["elevation"] = f"{site.elevation_m} m ({site.elevation_datum})"
            else:
                properties["elevation"] = f"{site.elevation_m} m"

        # Add the location property if it exists
        location = ", ".join(
            part for part in [site.admin_area_2, site.admin_area_1, site.country] if part
        )
        if location:
            properties["location"] = location

        # Assemble the GeoJSON feature for the current site
        geojson_site = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [site.longitude, site.latitude],
            },
            "properties": properties,
        }

        # Add the populated GeoJSON feature to the FeatureCollection
        geojson_site_feature_collection['features'].append(geojson_site)

    # Return the constructed GeoJSON FeatureCollection for the workspace's sites
    return geojson_site_feature_collection


def date_clamp_to_datastream(date: datetime | Literal["latest"] | None, datastream: Datastream) -> datetime | None:
    """
    Clamp the given date to the bounds of the datastream's phenomenon times.

    Args:
        date (datetime | Literal["latest"]): The date to clamp. Can be a datetime object or the string "latest".
        datastream: The datastream object containing phenomenon_begin_time and phenomenon_end_time.

    Returns:
        datetime | None: The clamped date or None if not provided.
    """
    # Return None if date is not provided
    if not date:
        return None

    # Check for "latest" string
    if isinstance(date, str) and date == "latest":
        # Return the end of the datastream if "latest" is specified
        return datastream.phenomenon_end_time

    # Make sure the date is not before the start of the datastream
    if datastream.phenomenon_begin_time and date < datastream.phenomenon_begin_time:
        return datastream.phenomenon_begin_time

    # Make sure the date is not after the end of the datastream
    if datastream.phenomenon_end_time and date > datastream.phenomenon_end_time:
        return datastream.phenomenon_end_time
    
    # If the date is within the bounds of the datastream, return it as is
    return date
