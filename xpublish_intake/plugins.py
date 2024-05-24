import logging
from typing import Sequence

import intake
import xarray as xr
import tempfile
import yaml
from fastapi import APIRouter, Depends, Request, Response
from starlette.routing import NoMatchFound
from xpublish.plugins import Dependencies, Plugin, hookimpl
from xpublish.utils.api import DATASET_ID_ATTR_KEY

logger = logging.getLogger('intake_catalog')


def get_dataset_id(ds):
    xpublish_id = ds.attrs.get(DATASET_ID_ATTR_KEY)
    cf_dataset_id = ".".join(
        [
            x for x in [
                ds.attrs.get('naming_authority'),
                ds.attrs.get('id')
            ] if x
        ]
    )

    dataset_id_options = [
        xpublish_id,
        cf_dataset_id,
        'dataset'
    ]

    return next(x for x in dataset_id_options if x)


def get_zarr_source(xpublish_id, request):
    url = ''
    try:
        from xpublish.plugins.included.zarr import ZarrPlugin  # noqa
        url = request.url_for("get_zarr_metadata")
    except NoMatchFound:
        # On multi-dataset servers add the dataset_id to the route
        url = request.url_for("get_zarr_metadata", dataset_id=xpublish_id)

    # Convert url object from <class 'starlette.datastructures.URL'> to a string
    url = str(url)

    # Remove .zmetadata from the URL to get the root zarr URL
    url = url.replace("/.zmetadata", "")

    if not url:
        return {}

    return url


class IntakePlugin(Plugin):
    """Adds an Intake catalog endpoint"""

    name: str = 'intake_catalog'
    dataset_metadata: dict = dict()

    app_router_prefix: str = '/intake'
    app_router_tags: Sequence[str] = ['intake']

    dataset_router_prefix: str = ''
    dataset_router_tags: Sequence[str] = ['intake']

    @hookimpl
    def app_router(self, deps: Dependencies):
        """Register an application level router for app level intake catalog"""
        router = APIRouter(prefix=self.app_router_prefix, tags=self.app_router_tags)

        def get_request(request: Request) -> str:
            return request

        @router.get(".yaml", summary="Root intake catalog")
        def get_root_catalog(
            request=Depends(get_request),
            dataset_ids = Depends(deps.dataset_ids)
        ):

            # ADD METADATA IN
            metadata = {
                'source': 'Served via `xpublish-intake`',
                'access_url': str(request.url),
            }

            cat = intake.entry.Catalog(metadata=metadata)

            for dataset_id in dataset_ids:
                url = get_zarr_source(dataset_id, request)
                if not url:
                    continue
                data = intake.datatypes.Zarr(url, metadata={})
                reader = data.to_reader("xarray", consolidated=True)
                cat[f'{dataset_id}'] = reader

            return Response(yaml.dump(cat.to_dict()), media_type="text/yaml")

        return router

    @hookimpl
    def dataset_router(self, deps: Dependencies):
        router = APIRouter(prefix=self.dataset_router_prefix, tags=list(self.dataset_router_tags))

        def get_request(request: Request) -> str:
            return request

        @router.get('/catalog.yaml', summary="Dataset intake catalog")
        def get_dataset_catalog(
            request=Depends(get_request),
            dataset=Depends(deps.dataset),
        ):
            xpublish_id = get_dataset_id(dataset)

            # ADD METADATA IN

            cat = intake.entry.Catalog()
            urls = {
                'zarr': get_zarr_source(xpublish_id, request)
            }

            for k, url in urls.items():
                if not url:
                    continue

                data = intake.datatypes.Zarr(url, metadata={})
                reader = data.to_reader("xarray", consolidated=True)
                cat[f'{xpublish_id}'] = reader

            return Response(yaml.dump(cat.to_dict()), media_type="text/yaml")

        return router
