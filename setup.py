"""Setup skyq_hub package."""
from setuptools import setup, find_namespace_packages

from pyskyqhub.version import __version__ as version

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyskyqhub',
    version=version,
    author='Roger Selwyn',
    author_email='roger.selwyn@nomail.com',
    description='Library for Sky Q hub',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/RogerSelwyn/skyq_hub',
    license='MIT',
    packages=find_namespace_packages(exclude=['tests','manage']),
    install_requires=['aiohttp>=3.6.2'],
    keywords='SKYQ hub',
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.7'	
)
