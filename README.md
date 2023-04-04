# xpublish-intake

An [`xpublish`](https://github.com/xarray-contrib/xpublish) plugin for serving intake catalogs

## Installation

For `conda` users you can

```shell
conda install --channel conda-forge xpublish_intake
```

or, if you are a `pip` users

```shell
pip install xpublish_intake
```

## Usage

The `intake` plugin is by default configured with

* `app_router_prefix='/intake'` which creates the `/intake.yaml` route for the root `intake` catalog containing all datasets in an `xpublish.Rest` instance. By default that route is available at `http://.../intake.yaml`.

* `dataset_router_prefix=''` which creates an `/datasets/[name]/catalog.yaml` router for all datasets in the `xpublish.Rest` instance. By default those route are available at `http://.../datasets/[name]/catalog.yaml`.

## Get in touch

Report bugs, suggest features or view the source code on [GitHub](https://github.com/axiom-data-science/xpublish_intake/issues).

## License and copyright

`xpublish_intake` is licensed under the MIT License.

Development occurs on GitHub at <https://github.com/axiom-data-science/xpublish_intake>.
