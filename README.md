# tethysdash-plugin-hydroserver

A Tethys Dash plugin that provides a collection of HydroServer visualizations

> [!WARNING]
> **The HydroServer API key is currently a plugin argument, and plugin arguments are not secret.**
> Tethys Dash stores every argument value in the dashboard's saved configuration and sends it to
> the browser (as of version 0.20.2, via a GET request), so anyone who can view or edit a dashboard
> that uses this plugin can read the API key you entered.

Until this is addressed (see below), take the following precautions when using this plugin:

- **Use a least-privilege API key.** Create a dedicated, **read-only**, workspace-scoped key for the
  dashboard rather than reusing a key with broader permissions or your account credentials.
- **Treat the key as disposable.** Be ready to **revoke and rotate** it if a dashboard is shared more
  widely than intended. Keys can be managed (created, listed, revoked) per workspace in HydroServer.
- **Do not share or export a dashboard that contains a real key.** The value is persisted in the
  dashboard configuration, so sharing the dashboard shares the key.

### Planned fix

A future release of Tethys Dash (after `0.20.2`) will add a feature to safeguard sensitive plugin
arguments. Once that functionality is available, this plugin will be updated to use it, and the 
precautions above will no longer be necessary. Until then, the guidance above applies.

## HydroServer Datastream Plot

The **HydroServer Datastream Plot** visualization plots a single datastream's observations over time
as a Plotly line chart. You configure it with the HydroServer host URL, an API key, and the
datastream's id, plus an optional start and end date to limit the time range.

The y-axis is labeled with the datastream's observed property and unit (for example,
`Temperature (degC)`), and the x-axis is the observation date. If the observed property or unit can't
be read, the axis falls back to `Unknown`, and if the datastream has no observations in the selected
range the chart renders empty with a "No Data" label rather than failing.

Dates are clamped to the datastream's available period: a start or end date earlier or later than the
datastream's own range is pulled back to that range, and if a date is omitted the datastream's full
period is used. This means you can pick any date when configuring the dashboard without having to know
the datastream's exact extent up front.

## HydroServer Sites Map

The **HydroServer Sites Map** visualization plots the monitoring sites in a workspace as points on a
map. Each site's popup shows its name, code, type, and (when available) description, elevation, and
location. Clicking a site publishes its id to the `HydroServer Site` dashboard variable, so other
components on the dashboard can react to the selection.

### Site type symbology

Each site is symbolized by its `site_type` so the different kinds of sites are distinguishable at a
glance, and this happens automatically:

- Common HydroServer/ODM2 site types are shown with a predefined shape and color.
- Any other site type is automatically given its own distinct shape and color.
- Sites with no site type are shown as a neutral gray circle.

The legend lists only the site types actually present in the workspace, so it always matches what is
on the map. No setup is required — unusual or previously unseen site types are distinguished on their
own.

The predefined symbols for common site types are:

| Site type                    | Shape    | Color     |
| ---------------------------- | -------- | --------- |
| Stream                       | triangle | `#4e79a7` |
| Lake, Reservoir, Impoundment | square   | `#59a14f` |
| Spring                       | star     | `#b07aa1` |
| Well                         | diamond  | `#9c755f` |
| Atmosphere                   | cross    | `#f28e2b` |
| Wetland                      | x        | `#76b7b2` |

## HydroServer Sites Map Layer

The **HydroServer Sites Map Layer** adds a workspace's monitoring sites to an existing map
as a single layer, rather than rendering its own map. You add it to a map in the layer
editor, where it pre-fills the layer's style, legend, and popup settings; from there the
Style, Labels, Legend, and Attributes tabs are yours to adjust.

Unlike the standalone Sites Map, this layer is dynamic: it re-fetches the workspace's sites
each time the map renders, so added, moved, or removed sites stay current without
reconfiguring the dashboard. The popup fields, the `HydroServer Site` click variable,
and the site-type symbology all behave the same as the Sites Map visualization.

The site-type symbology is a snapshot taken when the layer is configured, reflecting the
site types present at that time. If a brand-new site type appears afterward, its sites still
show on the map but use the default gray symbol and are absent from the legend until the
layer is reconfigured.

## HydroServer Datastream Dropdown

The **HydroServer Datastream Dropdown** is a variable input that lets a dashboard viewer pick a
datastream from a workspace. You configure it with the HydroServer host URL, an API key, and the
workspace id; it fetches the workspace's datastreams and lists them in a dropdown, each labeled by
its site as `Site Name - Datastream Name` and sorted alphabetically.

The selected datastream's id is published to the `HydroServer Datastream` dashboard variable, which
other components reference with `${HydroServer Datastream}`. The intended pairing is the HydroServer
Datastream Plot: set the plot's datastream id argument to `${HydroServer Datastream}` and the chart
updates whenever a different datastream is picked.

Because a plugin input re-runs whenever its arguments change, the workspace can itself come from
another variable input — set the dropdown's workspace id to a `${...}` reference and the datastream
list repopulates when the upstream workspace selection changes.
