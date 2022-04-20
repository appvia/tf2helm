# tf2helm

`t2helm` is a simple Python utility that converts a Terraform module to a Helm Chart. The Helm Chart contains a Kubernetes Custom Resource understood and managed by the [Terraform Operator](https://github.com/isaaguilar/terraform-operator) at present and it will soon be extended to support other similar operators e.g. [oam-dev Terraform Controller](https://github.com/oam-dev/terraform-controller).

`tf2helm` reads a Terraform module from a local or remote path and converts it into a Helm chart in a specified directory. It reads the Terraform variables and writes them as `.Values.required` and `.Values.optional` values in the Helm `values.yaml` file depending on whether they have been assigned values or not.

This gives infrastructure operators e.g. DevOps or Platform engineers the flexibility to set sensible default parameters for cloud resources and make them visible and configurable to application developers who may or may not override them afterwards.

## Installation

```
pip install tf2helm
```

## Usage
```
$ tf2helm --help
Usage: tf2helm [OPTIONS]

  tf2helm converts a Terraform module to a Helm Chart [currently only supports
  the Terraform Operator]


Options:
  --tf_module TEXT          Path or URL to a Terraform module.
  --tf_module_url TEXT      Specify this if tf_module does not point to a URL.
  --tf_module_version TEXT  Terraform module version.
  --tf_version TEXT         Terraform version.
  --name TEXT               Helm chart name.
  --version TEXT            Helm chart version.
  --app_version TEXT        Helm chart application version.
  --output_dir TEXT         Path to the Helm chart output directory.
  --help                    Show this message and exit.
```
