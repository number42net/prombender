from setuptools import setup, find_packages

setup(
    name='prombender',
    version='1.0',
    package_dir={"": "src"},
    packages=find_packages(),
    entry_points = {
        'console_scripts': ['prombender=prombender.command_line:main'],
    }
)