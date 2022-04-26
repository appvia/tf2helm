#!/usr/bin/env python

import os
import shutil
import requests
from jinja2 import Environment, FileSystemLoader
from git import Repo


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


def download_tf_module(module, output_dir, env=None):
    """
    Assumes source code is stored Git.
    Clones your Git repository into a specified directory.
    Arguments:
        module: terraform module URL
        output_dir: an absolute or relative path to where the terraform module will be stored
    """
    repo_url = module.split('?')[0]
    repo_name = repo_url.split('/')[-1].split('.')[0]
    output_dir = output_dir + '/' + repo_name
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    if len(module.split('?')) > 1:
        ref = module.split('?')[1].split('=')[1]
        repo = Repo.clone_from(repo_url, output_dir, env=env)
        repo.git.checkout(ref)
    else:
        Repo.clone_from(repo_url, output_dir, env=env)
    return repo_name
