import pytest
import xarray as xr
from xpublish.plugins import manage

from .utils import DatasetTester


def test_import_plugin():
    plugins = manage.load_default_plugins()
    assert 'intake' in plugins


class TestOneIntake(DatasetTester):

    @pytest.fixture(scope='module')
    def dataset(self):
        ds = xr.Dataset({'count': ('x', [1, 2, 3])})
        yield ds
