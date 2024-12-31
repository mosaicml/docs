# FAQ

<!-- TODO: update -->
We've aggregated questions frequently asked by our customers in this page. If you have a question that is not answered anywhere in our documentation, reach out to us through our [Community Slack](https://join.slack.com/t/mosaicml-community/shared_invite/zt-w0tiddn9-WGTlRpfjcO9J5jyrMub1dg).

## Onboarding
After signing a sales agreement, you'll receive an email with instructions to onboard through [MosaicML Console](https://console.mosaicml.com/). The email lists the following steps:
  1. Go to the [MosaicML Console](https://console.mosaicml.com/)
  2. Authenticate with either SSO or Continue with Google option.
  3. Read and accept the terms of service.
  4. Once you have accepted the terms, you'll enter our Quick Start onboarding process. This will walk you through the following:
      1. Setting up the MosaicML Command Line Interface (MCLI)
      2. Getting your API key and configuring it on your development environment
      3. Submitting your first "Hello World!" training run. This verifies you have access to the cluster.
      4. Submitting a large language model (LLM) training run. This verifies your set up is fully operational.

## What are Clusters and Runs?
A cluster is one or more nodes with the same type of GPU (e.g. A100-40GB) residing in a supported cloud provider. MosaicML has several types of clusters:
  1. **Shared Cluster:** Shared clusters allow multiple customers to use up to two nodes for their jobs. If the cluster is at max capacity then jobs will be queued and run when resources become available.
  2. **Reserved Cluster:** Reserved cluster's resources are dedicated 24x7 to a single customer and fully managed by MosaicML.
  3. **3rd Party (3P) Cluster:** 3rd Party clusters are dedicated to and managed by the customer and their chosen cloud provider such as AWS or CoreWeave. The nodes in the cluster are dedicated to running MosaicML workloads, and are orchestrated by the MosaicML platform.  

Runs are model training jobs. When you submit a run, the MosaicML platform will request resources from the cluster. If none of the requested resources are available, the run will be queued. To learn more about clusters see the [Managing Compute](https://docs.mosaicml.com/projects/mcli/en/latest/quick_start/managing_clusters.html) page. For detailed run information, see the [Configure a run](https://docs.mosaicml.com/projects/mcli/en/latest/training/yaml_schema.html) page.

## Is using Composer required in order to train a model on the MosaicML platform?
No, Composer is not required. You can use any training framework, and more broadly speaking the MosaicML platform can deploy any Docker image as long as it has all the required system packages for your code. For more information, see the [Docker documentation](https://docs.docker.com/) and the [MosaicML Docker guide](https://docs.mosaicml.com/projects/mcli/en/latest/resources/secrets/docker.html).

## How do I configure my training run to access private GitHub repositories, Docker images, S3, Weights & Biases, etc.?
To access private GitHub repositories, Docker images, or other integrations, you may need to provide secrets. Secrets are kept securely in the MosaicML platform and are available across your clusters. For more details, see the [Secrets Page](https://docs.mosaicml.com/projects/mcli/en/latest/resources/secrets/).

## How do I set up an environment in MosaicML platform to run my code?
Setting up the environment in MosaicML platform is straightforward and easily configurable. We'll automatically set up environment variables in your run container. To add other environment variables, use the `env_variable` field in the YAML file. For more information, see the [Environment Setup guide](https://docs.mosaicml.com/projects/mcli/en/latest/quick_start/environment.html).

## What are the supported MosaicML integrations?
MosaicML platform supports various integrations, such as Git repositories, APT packages, Pip packages, and Weights & Biases. For more information, see the following pages:

- [Git Repo Page](https://docs.mosaicml.com/projects/mcli/en/latest/resources/integrations/git.html)
- [Apt Packages Page](https://docs.mosaicml.com/projects/mcli/en/latest/resources/integrations/system_dependencies.html)
- [CometML](https://docs.mosaicml.com/projects/mcli/en/latest/resources/integrations/comet.html)
- [PyPI Packages](https://docs.mosaicml.com/projects/mcli/en/latest/resources/integrations/pypi.html)
- [WandB Packages Page](https://docs.mosaicml.com/projects/mcli/en/latest/resources/secrets/wandb.html)