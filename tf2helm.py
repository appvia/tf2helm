#!/usr/bin/env python

import tfparser
import filehandler
import json
import yaml
import os
import time
import configparser
import fire
from avionix import ChartBuilder, ChartInfo, Values
from avionix.kube.base_objects import KubernetesBaseObject
from halo import Halo


config = configparser.ConfigParser()
config.read('config.ini')
spinner = Halo(spinner='dots')


def convert(tf_module, tf_module_version, tf_version, name, version, app_version, output_dir):
    '''
    tf2helm converts a Terraform module to a Helm Chart [currently only supports the Terraform Operator]

    :param tf_module: absolute or relative path to a Terraform module
    :param tf_module_version: terraform module version
    :param tf_version: terraform version used for creating the resources
    :param name: helm chart name
    :param version: helm chart version
    :param app_version: helm chart application version
    :param output_dir: absolute or relative path to where the Helm chart will be created
    '''
    tf_config = {}
    tf_config['tf_module'] = tf_module
    tf_config['tf_module_version'] = tf_module_version
    tf_config['tf_version'] = tf_version

    try:
        if tf_module.startswith('https://'):
            spinner.start(config.get('stages', 'setup'))
            time.sleep(1)
            tf_module = filehandler.download_tf_module(
                tf_module, tf_module_version, '.modules')
            spinner.succeed()

        spinner.start(config.get('stages', 'translate'))
        time.sleep(1)
        required_tf_vars, optional_tf_vars = tfparser.get_tf_vars(
            '.modules/' + tf_module)
        spinner.succeed()
        spinner.start(config.get('stages', 'create'))
        time.sleep(1)
        dict = {**required_tf_vars, **optional_tf_vars}
        values = Values(dict)
        builder = ChartBuilder(ChartInfo(api_version="v2", name=name,
                               version=version, app_version=app_version), [], values=values,
                               output_directory=output_dir)
        builder.generate_chart()
        spinner.succeed()
        spinner.start(config.get('stages', 'update'))
        time.sleep(1)
        filehandler.render_template('tf_operator.yaml.j2', required_tf_vars, tf_config,
                                    output_dir + '/' + name + '/templates/' + name + '.yaml')
        filehandler.copy_file(
            'files/_helpers.tpl', output_dir + '/' + name + '/templates/')
        spinner.succeed()
        spinner.stop_and_persist(symbol='🚀'.encode(
            'utf-8'), text="Helm Chart is available at %s/%s" % (output_dir, name))
    except (KeyboardInterrupt, SystemExit):
        spinner.stop()


if __name__ == '__main__':
    fire.core.Display = lambda lines, out: print(*lines, file=out)
    fire.Fire({
        'convert': convert
    })
