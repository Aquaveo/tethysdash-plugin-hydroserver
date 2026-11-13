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
