from setuptools import setup


setup(
    entry_points={
        'xpublish.plugin': [
            'intake = xpublish.plugins.axds.intake:IntakePlugin',
        ]
    },
)
