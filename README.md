# xpublish-intake

An [`xpublish`](https://github.com/xarray-contrib/xpublish) plugin for serving intake catalogs

## Why?

As data access services are moved from custom APIs into `xpublish` plugins, data users need a way to discover these new plugins as they become available without changing their analysis code. One way to standardize dataset access for those that can be loaded via [`intake`](https://intake.readthedocs.io/en/latest/index.html) is to provide an `intake` catalog of the plugins endpoints.

## Ideas

This plugin currently supports the `xpublish.plugins.included.zarr.ZarrPlugin` plugin (which is `intake` compatible). In the future it would be nice if this library did not have to understand each and every plugin that is `intake` compatible and left it up to the plugin authors to add `intake` catalog support into their access services where applicable. This library could provide a mixin for `xpublish` plugins to use to register their endpoints in a standard way to then be advertised in an `intake` catalog.

## Installation

For `conda` users you can

```shell
conda install --channel conda-forge xpublish_intake
```

or, if you are a `pip` user

```shell
pip install xpublish_intake
```

## Setup

The `intake` plugin will be automatically discoverd by `xpublish` if you have the library installed. This will work for most users if you don't need to customize the endpoints.

If you specify your plugins manually you will need to add `IntakePlugin` to the `plugins` argument of `xpublish.Rest` or register the `IntakePlugin` explicitly.

```python

from xpublish_intake.plugins import IntakePlugin

# Included in the `plugins` map
rest = Rest(
    ...
    plugins={
        ...
        'intake': IntakePlugin()
    }
)

# Registered explicitly
rest = Rest(...)
rest.register_plugin(IntakePlugin())
```

## Usage

The `intake` plugin is by default configured with

* `app_router_prefix='/intake'` which creates the `/intake.yaml` route for the root `intake` catalog containing all datasets in an `xpublish.Rest` instance. By default that route is available at `http://.../intake.yaml`.

* `dataset_router_prefix=''` which creates an `/datasets/[name]/catalog.yaml` router for all datasets in the `xpublish.Rest` instance. By default those route are available at `http://.../datasets/[name]/catalog.yaml`.

## Get in touch

Report bugs, suggest features or view the source code on [GitHub](https://github.com/axiom-data-science/xpublish-intake/issues).

## License and copyright

`xpublish_intake` is licensed under the MIT License.

Development occurs on GitHub at <https://github.com/axiom-data-science/xpublish-intake>.
