#!/usr/bin/env python

import os
import shutil
import requests
import zipfile
from jinja2 import Environment, FileSystemLoader
from io import BytesIO


def render_template(filename, config, tf_config, chart_filename):
    """
    Renders a template based on provided configuration and writes it to the Helm Chart directory
    Arguments:
        filename: name of a file saved under the templates/ directory
        config: a set of configuration used to render the template
        chart_filename: an absolute or relative path to the rendered file in the Helm Chart directory
    """
    file_loader = FileSystemLoader(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "templates"))
    env = Environment(loader=file_loader)
    template = env.get_template(filename)
    custom_resource = template.render(config=config, tf_config=tf_config)
    with open(chart_filename, 'w') as f:
        f.write(custom_resource)


def copy_file(source, destination):
    """
    Copies a file from a source to a destination directory
    Arguments:
        source: an absolute or relative path to the source file
        destination: an absolute or relative path to the destination file
    """
    shutil.copy2(source, destination)


def download_tf_module(module, version, output_dir):
    """
    Assumes source code is stored Git.
    Downloads it as a zip file and unzips it in a specified directory.
    Arguments:
        module: terraform module URL
        version: terraform module version
        output_dir: an absolute or relative path to where the terraform module will be stored
    """
    if module.endswith('/'):
        module.strip('/')
    if not version.startswith('v'):
        version = 'v' + version
    url = module + '/archive/refs/tags/' + version + '.zip'
    response = requests.get(module + '/archive/refs/tags/' + version + '.zip')
    archive = zipfile.ZipFile(BytesIO(response.content))
    archive.extractall(output_dir)
    return archive.namelist()[0]
