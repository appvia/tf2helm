# tf2helm

`t2helm` is a simple Python utility that converts a Terraform module to a Helm Chart. The Helm Chart contains a Kubernetes Custom Resource understood and managed by one of the following Kubernetes Operators:
1. [Isaaguilar Terraform Operator](https://github.com/isaaguilar/terraform-operator)
2. [Open Application Model Terraform Controller](https://github.com/oam-dev/terraform-controller)
3. [Appvia Terraform Controller](https://github.com/appvia/terraform-controller)

`tf2helm` reads a Terraform module from a local or remote path and converts it into a Helm chart in a specified directory. It reads the Terraform variables and writes them as `.Values.required` and `.Values.optional` values in the Helm `values.yaml` file depending on whether they have been assigned values or not.

This gives infrastructure operators e.g. DevOps or Platform engineers the flexibility to set sensible default parameters for cloud resources and make them visible and configurable to application developers who may or may not override them afterwards.

## Installation

```
pip install tf2helm
```

## Usage
```
tf2helm
Usage: tf2helm [OPTIONS]

  tf2helm converts a Terraform module to a Helm Chart [currently only supports
  the Terraform Operator]

Options:
  --tf_module_path TEXT  Terraform module local Path e.g.
                         "/local/path/to/module".
  --tf_module_url TEXT   Terraform module URL e.g.

                         "https://github.com/<org>/<module>?ref=<branch|tag>".
  --tf_version TEXT      Terraform version.
  --git_auth TEXT        Git access token or SSH private key to use with a
                         private repository.
  --template TEXT        Template to generate the custom resource definition.
                         (isaaguilar, terraform-controller, oam-terraform-
                         controller)
  --name TEXT            Helm chart name.
  --version TEXT         Helm chart version.
  --app_version TEXT     Helm chart application version.
  --output_dir TEXT      Path to the Helm chart output directory.
  --help                 Show this message and exit.
```
