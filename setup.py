import io
import os
import re

try:
    import setuptools
    setup = setuptools.setup
except ImportError:
    setuptools = None
    from distutils.core import setup

def read(name):
    return open(os.path.join(os.path.dirname(__file__), name)).read()

packages = [
    'wcs',
    'wcs.services',
    'wcs.commons',
]

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name='wcscmd',
    version=find_version("wcs/__init__.py"),
    description='Wangsu Cloud Storage Command Tool',
    long_description='see:\nhttps://wcs.chinanetcenter.com/document/SDK\n',
    author='ChinaNetCenter.Wangsu Cloud Strage',
    maintainer = 'https://github.com/Wangsu-Cloud-Storage',
    author_email = 'cdn_team_storage_wcs@chinanetcenter.com',
    url='https://wcs.chinanetcenter.com/document/SDK',
    packages=packages,
    scripts=['wcscmd'],
    license = 'MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires=['requests>=2.11.1','poster','logging','argparse', 'lockfile', 'requests_toolbelt','pyyaml'],
    
    entry_points={
        'console_scripts':[
            'wcs_etag_cal = wcs.commons.etag_files:main',
        ]
    }
)
