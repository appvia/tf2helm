#!/usr/bin/env python

import glob
import hcl2
import os
from avionix import ChartBuilder, ChartInfo, Values


def get_tf_files(module):
    """
    Gets all terraform files (.tf) in a given module
    Arguments:
        module: an absolute or relative path to a terraform module
    Returns:
        A list of identified terraform files (.tf)
    """
    tf_files = [os.path.join(module, f)
                for f in os.listdir(module) if f.endswith(".tf")]
    return tf_files


def get_tf_vars_files(module):
    """
    Gets all terraform variable definitions (.tfvars) in a given module
    Arguments:
        module: an absolute or relative path to a terraform module
    Returns:
        A list of identified terraform variable definition files (.tfvars)
    """
    tf_vars_files = [os.path.join(module, f) for f in os.listdir(
        module) if f.endswith(".tfvars")]
    return tf_vars_files


def does_tf_var_have_a_val(module, variable):
    """
    Checks whether a terraform variable has a value assigned to it
    Arguments:
        module: an absolute or relative path to a terraform module
        variable: a terraform variable from the specified terraform module
    Returns:
        A terraform variable if it has a value assigned to it
    """
    for f in get_tf_vars_files(module):
        with open(f, 'r') as file:
            dict = hcl2.load(file)
            for k, v in dict.items():
                if k == variable:
                    return v


def get_tf_vars(module):
    """
    Gets all required terraform variables
    Arguments:
        module: an absolute or relative path to a terraform module
    Returns:
        A dictionary containing a set of dictionaries with required and optional terraform variables and their default values
    """
    tf_vars = {'required': {}, 'optional': {}}
    for f in get_tf_files(module):
        with open(f, 'r') as file:
            dict = hcl2.load(file)
            if 'variable' in dict:
                for var in dict['variable']:
                    for k in var:
                        if 'default' in var.get(k):
                            v = does_tf_var_have_a_val(module, k)
                            if v is None:
                                tf_vars['optional'][k] = var.get(k)['default']
                            else:
                                tf_vars['optional'][k] = v
                        else:
                            v = does_tf_var_have_a_val(module, k)
                            if v is None:
                                tf_vars['required'][k] = ""
                            else:
                                tf_vars['optional'][k] = v
    return tf_vars
