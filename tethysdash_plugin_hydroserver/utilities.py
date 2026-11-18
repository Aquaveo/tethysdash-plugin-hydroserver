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
