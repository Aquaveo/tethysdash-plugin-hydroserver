from tethysdash_plugin_hydroserver.schemas import SiteSymbol


# Shared point-marker styling applied to every site
POINT_SIZE = 7
POINT_STROKE_COLOR = "#ffffff"
POINT_STROKE_WIDTH = 1

# Default symbol for sites without a curated type
DEFAULT_SITE_SYMBOL = SiteSymbol(shape="circle", fill="#bab0ac")

# Predefined symbols for common site types
CURATED_SITE_TYPE_SYMBOLS = {
    "Stream": SiteSymbol(shape="triangle", fill="#4e79a7"),
    "Lake, Reservoir, Impoundment": SiteSymbol(shape="square", fill="#59a14f"),
    "Spring": SiteSymbol(shape="star", fill="#b07aa1"),
    "Well": SiteSymbol(shape="diamond", fill="#9c755f"),
    "Atmosphere": SiteSymbol(shape="cross", fill="#f28e2b"),
    "Wetland": SiteSymbol(shape="x", fill="#76b7b2"),
}

# Symbols and colors used for automatically assigning distinct symbols to site types without a predefined symbol
_AUTO_SYMBOL_SHAPES = ["circle", "square", "triangle", "star", "diamond", "cross", "x"]
_AUTO_SYMBOL_COLORS = [
    "#4e79a7", "#f28e2b", "#59a14f", "#e15759", "#76b7b2",
    "#b07aa1", "#9c755f", "#edc948", "#ff9da7", "#bab0ac",
]


def _auto_symbol_palette_build() -> list[SiteSymbol]:
    """
    Build the palette of distinct shape+color symbols for uncurated site types.

    This function generates a list of shape+color pairs that are not already used by predefined site symbols.

    Returns:
        list[SiteSymbol]: A list of dictionaries representing distinct shape+color symbols for uncurated site types.
    """
    # Determine shape+color pairs already used by predefined symbols
    curated_pairs = {
        (symbol["shape"], symbol["fill"]) for symbol in CURATED_SITE_TYPE_SYMBOLS.values()
    }

    # Build the palette of distinct shape+color pairs for uncurated site types
    palette = []
    for step in range(len(_AUTO_SYMBOL_SHAPES) * len(_AUTO_SYMBOL_COLORS)):
        # Pair a shape and a color by the same stepping index
        shape = _AUTO_SYMBOL_SHAPES[step % len(_AUTO_SYMBOL_SHAPES)]
        fill = _AUTO_SYMBOL_COLORS[step % len(_AUTO_SYMBOL_COLORS)]

        # Skip combinations already used by a predefined symbol
        if (shape, fill) in curated_pairs:
            continue

        # Add the pair to the set of pairs
        palette.append(SiteSymbol(shape=shape, fill=fill))

    return palette


# Automatically generated symbol palette for uncurated site types
AUTO_SYMBOL_PALETTE = _auto_symbol_palette_build()


def sites_symbology_build(sites_feature_collection: dict) -> tuple[dict, dict | str]:
    """
    Build the rule-based style and matching legend for a sites GeoJSON layer.

    Every site type present is given its own symbol so the types are
    distinguishable on the map: common types use a predefined symbol, and any
    other type is automatically assigned a distinct one. Features with no site
    type use the default symbol. The legend lists only what is actually present.

    Args:
        sites_feature_collection (dict): A GeoJSON FeatureCollection of sites, as
            returned by ``hydroserver_workspace_sites_geojson_get``. Each feature's
            ``site_type`` property drives the symbology.

    Returns:
        tuple[dict, dict | str]: The style dict for ``set_style`` and the legend
            for ``set_legend`` (a legend dict, or the string "default" when there
            is nothing to distinguish).
    """
    # Collect the distinct site types present to build the symbology and legend
    present_site_types = []
    seen_site_types = set()
    has_untyped = False

    for feature in sites_feature_collection["features"]:
        # Get the current feature's site type
        site_type = feature["properties"].get("site_type")

        # Features without a site type render with the default symbol
        if not site_type:
            has_untyped = True
            continue

        # If the site type hasn't been seen before, add it to the list
        if site_type not in seen_site_types:
            seen_site_types.add(site_type)
            present_site_types.append(site_type)

    # Get the list of uncurated site types that need symbols from the auto palette
    symbol_by_site_type = {}
    uncurated_site_types = sorted(
        site_type
        for site_type in present_site_types
        if site_type not in CURATED_SITE_TYPE_SYMBOLS
    )

    # Assign symbols from the auto palette to uncurated site types
    for index, site_type in enumerate(uncurated_site_types):
        symbol_by_site_type[site_type] = AUTO_SYMBOL_PALETTE[index % len(AUTO_SYMBOL_PALETTE)]

    # Assign symbols for curated site types from the predefined mapping
    for site_type in CURATED_SITE_TYPE_SYMBOLS:
        symbol_by_site_type[site_type] = CURATED_SITE_TYPE_SYMBOLS[site_type]

    # Build a style rule and a legend item for each present site type
    rules = []
    legend_items = []

    for site_type in present_site_types:
        symbol = symbol_by_site_type[site_type]

        # Add a rule so this site type renders with its symbol
        rules.append(
            {
                "name": site_type,
                "geometryType": "point",
                "conditionField": "site_type",
                "conditionType": "=",
                "conditionValue": site_type,
                "shape": symbol["shape"],
                "fill": symbol["fill"],
                "size": POINT_SIZE,
                "stroke": POINT_STROKE_COLOR,
                "strokeWidth": POINT_STROKE_WIDTH,
            }
        )

        # Add a legend item for this site type
        legend_items.append(
            {"label": site_type, "color": symbol["fill"], "symbol": symbol["shape"]}
        )

    # Default style for features with no site type
    style = {
        "default": {
            "point": {
                "shape": DEFAULT_SITE_SYMBOL["shape"],
                "fill": DEFAULT_SITE_SYMBOL["fill"],
                "size": POINT_SIZE,
                "stroke": POINT_STROKE_COLOR,
                "strokeWidth": POINT_STROKE_WIDTH,
            }
        },
        "rules": rules,
    }

    # Add a legend entry for untyped features
    if has_untyped:
        legend_items.append(
            {
                "label": "Unspecified",
                "color": DEFAULT_SITE_SYMBOL["fill"],
                "symbol": DEFAULT_SITE_SYMBOL["shape"],
            }
        )

    # With no curated types to distinguish, fall back to the default legend
    legend = {"title": "Site Type", "items": legend_items} if legend_items else "default"

    # Return the constructed style and legend for the sites layer
    return style, legend
