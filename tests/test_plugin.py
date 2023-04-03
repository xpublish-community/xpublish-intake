from xpublish.plugins import manage


def test_import_plugin():
    plugins = manage.load_default_plugins()
    assert 'intake' in plugins
