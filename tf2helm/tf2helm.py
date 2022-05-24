#!/usr/bin/env python

from tf2helm import tfparser, filehandler
import json
import yaml
import os
import time
import click
import pkg_resources
from avionix import ChartBuilder, ChartInfo, Values
from avionix.kube.base_objects import KubernetesBaseObject
from halo import Halo


spinner = Halo(spinner='dots')


@click.command(no_args_is_help=True)
@click.option('--tf_module_path', default=None, help='Terraform module local Path e.g. "/local/path/to/module".')
@click.option('--tf_module_url', default=None, help='Terraform module URL e.g. "https://github.com/<org>/<module>?ref=<branch|tag>".')
@click.option('--tf_version', help='Terraform version.')
@click.option('--git_auth', help='Git access token or SSH private key to use with a private repository.')
@click.option('--template', default='isaaguilar', help='Template to generate the custom resource definition. (isaaguilar, terraform-controller, oam-terraform-controller)')
@click.option('--name', help='Helm chart name.')
@click.option('--app_version', help='Helm chart application version.')
@click.option('--output_dir', help='Path to the Helm chart output directory.')
@click.version_option()
def main(tf_module_path, tf_module_url, tf_version, git_auth, name, app_version, output_dir, template):
    """tf2helm converts a Terraform module to a Helm Chart"""
    tf_config = {}
    tf_config['tf_version'] = tf_version

    try:
        if tf_module_url:
            spinner.start('Download Terraform module')
            time.sleep(1)
            if git_auth:
                tf_config['git_repo'] = tf_module_url.split('?')[0]
                if os.path.isfile(os.path.expanduser(git_auth)) and tf_module_url.startswith('git'):
                    tf_module = filehandler.download_tf_module(tf_module_url, '.modules', env={'GIT_SSH_COMMAND':'ssh -i %s' % git_auth})
                elif not os.path.isfile(os.path.expanduser(git_auth)) and tf_module_url.startswith('https'):
                    url = 'https://' + git_auth + ':' + 'x-oauth-basic@' + tf_module_url.split('https://')[1]
                    tf_module = filehandler.download_tf_module(url, '.modules')
            else:
                tf_module = filehandler.download_tf_module(tf_module_url, '.modules')
            tf_config['tf_module'] = tf_module_url
            tf_module = '.modules/' + tf_module
            spinner.succeed()
        elif tf_module_path:
            tf_config['tf_module'] = None
            tf_module = tf_module_path
        spinner.start('Translate Terraform module')
        time.sleep(1)
        tf_vars = tfparser.get_tf_vars(tf_module)
        spinner.succeed()
        spinner.start('Create Helm Chart')
        time.sleep(1)
        values = Values(tf_vars)
        version = pkg_resources.require((__name__).split('.')[0])[0].version
        builder = ChartBuilder(ChartInfo(api_version="v2", name=name,
                               version=version, app_version=app_version), [], values=values,
                               output_directory=output_dir)
        builder.generate_chart()
        spinner.succeed()
        spinner.start('Update Helm Chart with Terraform Custom Resource')
        time.sleep(1)
        filehandler.render_template(template + '.yaml.j2', tf_vars, tf_config,
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
