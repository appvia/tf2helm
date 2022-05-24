#!/usr/bin/env python

from setuptools import setup


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='tf2helm',
    packages=['tf2helm'],
    version='0.0.18',
    description='tf2helm converts a Terraform module to a Helm Chart',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Mohammud Yassine Jaffoo',
    author_email='yassine.jaffoo@jaffoosolutions.com',
    url='https://github.com/appvia/tf2helm',
    py_modules=['tf2helm', 'tfparser', 'filehandler'],
    install_requires=['python-hcl2', 'avionix', 'requests',
                      'jinja2', 'halo', 'click', 'gitpython'],
    keywords=['terraform', 'helm', 'kubernetes',
              'self-service', 'cloud', 'aws', 'azure', 'gcp'],
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
    include_package_data=True,
    package_data={"": ["*.j2", "*.tpl"]},
    entry_points='''
        [console_scripts]
        tf2helm=tf2helm.tf2helm:main
    '''
)
