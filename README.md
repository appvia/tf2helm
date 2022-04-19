# tf2helm

`t2helm` is a simple Python utility that converts a Terraform module to a Helm Chart. The Helm Chart contains a Kubernetes Custom Resource understood and managed by the [Terraform Operator]() but `tf2helm` will soon be extended to support other similar operators.

![Alt Convert terraform module to a Helm chart](images/tf2helm.gif)

## Usage
```
./tf2helm.py convert -h
INFO: Showing help with the command 'tf2helm.py convert -- --help'.

NAME
    tf2helm.py convert - tf2helm converts a Terraform module to a Helm Chart [currently only supports the Terraform Operator]

SYNOPSIS
    tf2helm.py convert TF_MODULE TF_MODULE_VERSION TF_VERSION NAME VERSION APP_VERSION OUTPUT_DIR

DESCRIPTION
    tf2helm converts a Terraform module to a Helm Chart [currently only supports the Terraform Operator]

POSITIONAL ARGUMENTS
    TF_MODULE
        absolute or relative path to a Terraform module
    TF_MODULE_VERSION
        terraform module version
    TF_VERSION
        terraform version used for creating the resources
    NAME
        helm chart name
    VERSION
        helm chart version
    APP_VERSION
        helm chart application version
    OUTPUT_DIR
        absolute or relative path to where the Helm chart will be created

NOTES
    You can also use flags syntax for POSITIONAL ARGUMENTS
```
