import pytest
import xarray as xr
from xpublish.plugins import manage

from .utils import DatasetTester, SingleDatasetTester


def test_import_plugin():
    plugins = manage.load_default_plugins()
    assert 'intake' in plugins


class TestSimpleDataset(DatasetTester):

    @pytest.fixture(scope='module')
    def dataset(self):
        ds = xr.Dataset({'count': ('x', [1, 2, 3])})
        yield ds


class TestSimpleSingleDataset(SingleDatasetTester):

    @pytest.fixture(scope='module')
    def dataset(self):
        ds = xr.Dataset({'count': ('x', [1, 2, 3])})
        yield ds
