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

