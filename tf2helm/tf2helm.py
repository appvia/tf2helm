#!/usr/bin/env python

from tf2helm import tfparser, filehandler
import json
import yaml
import os
import time
import click
from avionix import ChartBuilder, ChartInfo, Values
from avionix.kube.base_objects import KubernetesBaseObject
from halo import Halo


spinner = Halo(spinner='dots')


@click.command()
@click.option('--tf_module', help='Path or URL to a Terraform module.')
@click.option('--tf_module_url', default=None, help='Specify this if tf_module does not point to a URL.')
@click.option('--tf_module_version', help='Terraform module version.')
@click.option('--tf_version', help='Terraform version.')
@click.option('--name', help='Helm chart name.')
@click.option('--version', help='Helm chart version.')
@click.option('--app_version', help='Helm chart application version.')
@click.option('--output_dir', help='Path to the Helm chart output directory.')
def main(tf_module, tf_module_version, tf_version, name, version, app_version, output_dir, tf_module_url):
    """tf2helm converts a Terraform module to a Helm Chart [currently only supports the Terraform Operator]"""
    tf_config = {}
    tf_config['tf_module_version'] = tf_module_version
    tf_config['tf_version'] = tf_version

    try:
        spinner.start('Download Terraform module')
        time.sleep(1)
        if tf_module.startswith('https://'):
            tf_config['tf_module'] = tf_module
            tf_module = filehandler.download_tf_module(
                tf_module, tf_module_version, '.modules')
            tf_module = '.modules/' + tf_module
        elif not tf_module.startswith('https://'):
            tf_config['tf_module'] = tf_module_url
        spinner.succeed()
        spinner.start('Translate Terraform module')
        time.sleep(1)
        required_tf_vars, optional_tf_vars = tfparser.get_tf_vars(tf_module)
        spinner.succeed()
        spinner.start('Create Helm Chart')
        time.sleep(1)
        dict = {**required_tf_vars, **optional_tf_vars}
        values = Values(dict)
        builder = ChartBuilder(ChartInfo(api_version="v2", name=name,
                               version=version, app_version=app_version), [], values=values,
                               output_directory=output_dir)
        builder.generate_chart()
        spinner.succeed()
        spinner.start('Update Helm Chart with Terraform Custom Resource')
        time.sleep(1)
        filehandler.render_template('tf_operator.yaml.j2', dict, tf_config,
                                    output_dir + '/' + name + '/templates/' + name + '.yaml')
        tpl = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "files", "_helpers.tpl")
        filehandler.copy_file(tpl, output_dir + '/' + name + '/templates/')
        spinner.succeed()
        spinner.stop_and_persist(symbol='🚀'.encode(
            'utf-8'), text="Helm Chart is available at %s/%s" % (output_dir, name))
    except (KeyboardInterrupt, SystemExit):
        spinner.stop()


if __name__ == '__main__':
    main()
