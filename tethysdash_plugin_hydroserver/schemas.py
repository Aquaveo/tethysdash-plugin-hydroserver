from typing import TypedDict


class SiteSymbol(TypedDict):
    """Represents a symbol for a site, including its shape and fill color."""
    shape: str
    fill: str
