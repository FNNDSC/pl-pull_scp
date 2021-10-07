from os import path
from setuptools import setup

with open(path.join(path.dirname(path.abspath(__file__)), 'README.rst')) as f:
    readme = f.read()

setup(
    name             = 'pull_scp',
    version          = '0.1',
    description      = 'This plugin application is used to recursively copy data from a remote host into an analysis root node.',
    long_description = readme,
    author           = 'Rudolph Pienaar -- FNNDSC',
    author_email     = 'rudolph.pienaar@childrens.harvard.edu',
    url              = 'http://wiki',
    packages         = ['pull_scp'],
    install_requires = ['chrisapp'],
    test_suite       = 'nose.collector',
    tests_require    = ['nose'],
    license          = 'MIT',
    zip_safe         = False,
    python_requires  = '>=3.6',
    entry_points     = {
        'console_scripts': [
            'pull_scp = pull_scp.__main__:main'
            ]
        }
)
