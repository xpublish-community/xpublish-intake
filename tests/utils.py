import pytest
import yaml
from fastapi.testclient import TestClient
from xpublish import Rest, SingleDatasetRest
from xpublish.plugins.included.zarr import ZarrPlugin

from xpublish_intake.plugins import IntakePlugin


class DatasetTester:

    DATASET_ID = 'ds'

    @pytest.fixture(scope='module')
    def dataset(self):
        pass

    @pytest.fixture(scope='module')
    def rest(self, dataset):
        dsmap = {
            self.DATASET_ID: dataset
        }
        rest = Rest(dsmap)
        rest.register_plugin(
            ZarrPlugin(dataset_router_prefix='/zarr'),
            overwrite=True
        )
        yield rest

    @pytest.fixture(scope='module')
    def dsid(self, dataset):
        return self.DATASET_ID

    @pytest.fixture(scope='module')
    def client(self, rest):
        client = TestClient(rest.app)
        yield client

    def test_intake_root(self, dsid, client):
        response = client.get('/intake.yaml')
        assert response.status_code == 200

        content = yaml.safe_load(response.text)
        # {
        #     "metadata": {
        #         "access_url": "http://testserver/intake.yaml",
        #         "source": "Served via `xpublish-intake`"
        #     },
        #     "sources": {
        #         "ds": {
        #             "args": {
        #                 "path": "http://testserver/datasets/ds/intake.yaml"
        #             },
        #             "description": "",
        #             "driver": "intake.catalog.local.YAMLFileCatalog",
        #             "metadata": {}
        #         }
        #     }
        # }

        assert content['metadata']['access_url'] == 'http://testserver/intake.yaml'

        assert dsid in content['sources']
        ds = content['sources'][dsid]
        assert ds['args']['path'] == f'http://testserver/datasets/{dsid}/catalog.yaml'
        assert ds['driver'] == 'intake.catalog.local.YAMLFileCatalog'

    def test_intake_dataset(self, dsid, client):
        response = client.get(f'/datasets/{dsid}/catalog.yaml')
        assert response.status_code == 200

        content = yaml.safe_load(response.text)
        # {
        #     "metadata": {
        #         "access_url": "http: //testserver/datasets/ds/intake.yaml",
        #         "source": "Served via `xpublish-intake`"
        #     },
        #     "name": "ds",
        #     "sources": {
        #         "ds-zarr": {
        #             "args": {
        #                 "consolidated": True,
        #                 "urlpath": "http://testserver/datasets/ds"
        #             },
        #             "description": "",
        #             "driver": "zarr"
        #         }
        #     }
        # }

        assert content['metadata']['access_url'] == f'http://testserver/datasets/{dsid}/catalog.yaml'
        assert content['name'] == dsid

        assert f'{dsid}-zarr' in content['sources']
        ds = content['sources'][f'{dsid}-zarr']
        assert ds['args']['urlpath'] == f'http://testserver/datasets/{dsid}/zarr'
        assert ds['driver'] == 'zarr'



class SingleDatasetTester(DatasetTester):
    @pytest.fixture(scope='module')
    def rest(self, dataset):
        rest = SingleDatasetRest(dataset)
        rest.register_plugin(
            ZarrPlugin(dataset_router_prefix='/zarr'),
            overwrite=True
        )
        yield rest

    @pytest.fixture(scope='module')
    def dsid(self):
        return 'dataset'

    def test_intake_root(self, dsid, client):
        response = client.get('/intake.yaml')
        assert response.status_code == 200

        content = yaml.safe_load(response.text)

        assert content['metadata']['access_url'] == 'http://testserver/intake.yaml'
        assert dsid in content['sources']
        ds = content['sources'][dsid]
        assert ds['args']['path'] == f'http://testserver/catalog.yaml'
        assert ds['driver'] == 'intake.catalog.local.YAMLFileCatalog'

    def test_intake_dataset(self, dsid, client):
        response = client.get(f'/catalog.yaml')
        assert response.status_code == 200

        content = yaml.safe_load(response.text)

        assert content['metadata']['access_url'] == f'http://testserver/catalog.yaml'
        assert content['name'] == dsid
        assert f'{dsid}-zarr' in content['sources']
        ds = content['sources'][f'{dsid}-zarr']
        assert ds['args']['urlpath'] == f'http://testserver/zarr'
        assert ds['driver'] == 'zarr'
