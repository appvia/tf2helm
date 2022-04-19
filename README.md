# tf2helm

`t2helm` is a simple Python utility that converts a Terraform module to a Helm Chart. The Helm Chart contains a Kubernetes Custom Resource understood and managed by the [Terraform Operator](https://github.com/isaaguilar/terraform-operator) at present and it will soon be extended to support other similar operators e.g. [oam-dev Terraform Controller](https://github.com/oam-dev/terraform-controller).

`tf2helm` reads a Terraform module from a local or remote path and converts it into a Helm chart in a specified directory. It reads the Terraform variables and writes them as `.Values.required` and `.Values.optional` values in the Helm `values.yaml` file depending on whether they have been assigned values or not.

This gives infrastructure operators e.g. DevOps or Platform engineers the flexibility to set sensible default parameters for cloud resources and make them visible and configurable to application developers who may or may not override them afterwards.

## Usage

![Alt convert the terraform module for AWS S3 bucket to a Helm Chart](images/tf2helm.gif)
