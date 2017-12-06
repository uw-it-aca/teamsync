import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='teamsync',
    version='1.0',
    packages=['teamsync'],
    include_package_data=True,
    install_requires = [
        'Django==1.10.2',
        'UW-RestClients-GWS>=0.3,<1.0'
    ],
    license='Apache License, Version 2.0',
    description='An application that syncs UW group memberships to GitHub teams',
    long_description=README,
    url='https://github.com/uw-it-aca/teamsync',
    author = "UW-IT AXDD",
    author_email = "aca-it@uw.edu",
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
)
