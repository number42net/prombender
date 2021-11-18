from setuptools import setup, find_packages

setup(
    name='prombender',
    version='1.0',
    packages=['prombender'],
    entry_points = {
        'console_scripts': ['prombender=prombender.command_line:main'],
    }
)