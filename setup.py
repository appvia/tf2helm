#!/usr/bin/env python

from distutils.core import setup

setup(
    name='tf2helm',
    packages=['tf2helm'],
    version='0.1.0',
    description='tf2helm converts a Terraform module to a Helm Chart [currently only supports the Terraform Operator]',
    author='Mohammud Yassine Jaffoo',
    author_email='yassine.jaffoo@jaffoosolutions.com',
    url='https://github.com/appvia/tf2helm',
    install_requires=['python-hcl2', 'avionix', 'requests', 'jinja2', 'fire', 'halo'],
    keywords = ['terraform', 'helm', 'kubernetes', 'self-service', 'cloud', 'aws', 'azure', 'gcp'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Text Processing",
    ],
)
