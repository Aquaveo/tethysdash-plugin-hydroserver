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
location. Clicking a site publishes its id to the `hydroserver_site_id` dashboard variable, so other
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
