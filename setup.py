from setuptools import setup

setup(
    entry_points={
        'xpublish.plugin': [
            'intake = xpublish_intake.plugins:IntakePlugin',
        ]
    },
)
