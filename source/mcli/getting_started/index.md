# Getting started
This guide will walk you through first time setup and getting started on Databricks Mosaic AI Training Platform


## Accessing Databricks Mosaic AI
All users added to an Organization on the Databricks Mosaic AI Training Platform will receive an email invite with instructions to access the [MosaicML Console](https://console.mosaicml.com/). 
The email expires within 7 days of receipt, so we encourage you to take action immediately. The email lists the following steps to follow to complete account setup:
1. Go to the [MosaicML Console](https://console.mosaicml.com/)
2. Authenticate with either SSO or Continue with Google option
3. Read and accept the terms of service
4. Once you have accepted the terms, you'll enter our Quick Start guide. This will walk you through the following:
    1. Setting up the MosaicML Command Line Interface (MCLI)
    2. Getting your API key and configuring it on your development environment
    3. Submitting your first "Hello World!" training run. This verifies you have access to the cluster
    4. Submitting a large language model (LLM) training run. This verifies your set up is fully operational

## Configuring your account secrets

Secrets allow you to inject sensitive values into your runs, such as API keys, passwords, or other access keys. These can be used to access your personal accounts for the various integrations we support. Secrets can be configured as an environment variable or through a mounted file, and are automatically available to every run, across clusters. Secrets are set by users and cannot be shared across users. We recommend configuring critical secrets as you're getting familiar with our platform, so you can use them for all future runs. 

Check out our detailed [Secrets Guide](secrets.md) for more details on how to configure specific secrets. 

## Prepare for a run
You can learn even more about how to work with runs in these sections:
* [Preparing for a run](../run_commands/index.md)
* [Submitting a run](../submitting_run/index.md)

## Managing User Permissioning
### `User` Role
Users manually added to a Mosaic Organization are automatically assigned a generic `user` role with access to:
- **Manage individual user's API keys:** Ability to create new API keys and user secrets
- **Manage individual user's runs:** Ability to read, update, and delete their own runs
- **Read Organization Runs:** Ability to read organizational runs (enabled if shared runs are active)

### `Administrator` Role
A `user` can be promoted to an `administrator` role by an existing Mosaic Organization Administrator. The `administrator` role has access to:
- **All `User` Permissions:** All permissions provided to the `User` role
- **Read All Organization Details:** Ability to view the organization's users, user invites, and organization details
- **Manage All Organization `Users`:** Ability to invite new users, change user roles, and remove existing users.
- **Manage All Organization Runs:** Ability to read, update, and delete user runs

Note that the Technical Contact on your Databricks Mosaic AI Training Platform contract was automatically assigned the `administrator` role in order to streamline your team's access to your Mosaic Organization. If you are having access issues, please contact your internal Databricks account representative.


## Getting familiar with our terminology

### What are Clusters?
A cluster is one or more nodes with the same type of GPU (e.g. H100-80GB) residing in a supported cloud provider. Databricks Mosaic AI Platform has 2 types of clusters:
  1. **Shared Cluster:** Shared clusters allow multiple customers to use up to 8 nodes for their jobs. If the cluster is at max capacity, then jobs will be queued and run when resources become available.
  2. **Reserved Cluster:** Reserved clusters are dedicated 24x7 to a single customer and fully managed by Databricks.

### What are Runs?
Runs are model training jobs. When you submit a run, the Databricks Mosaic AI Training Platform will request resources from the cluster. The status of a run can be managed through MCLI or the Python SDK, including creation, following, getting, and stopping the run.

#### What is the Run Lifecycle?
| Run Status  | Details                                                                                                                                                                                                |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Pending     | The run has been submitted but hasn’t been assigned a space in the queue.                                                                                                                              |
| Queued      | The run has been placed in the run queue to be picked up by the specified cluster. Runs may immediate start, but also could sit in this status indefinitely if the cluster is experiencing high demand |
| Starting    | The run has been scheduled and assigned nodes. This status includes setting up everything needed to run the workload, including setting up containers, pulling the docker image, etc.                  |
| Running     | Core phase where the run command is executed inside containers on one or more nodes.                                                                                                                   |
| Terminating | Before being terminated, runs will always enter a “terminating” status.                                                                                                                                |
| Completed   | The run has executed the full command and finished without any errors.                                                                                                                                 |
| Stopped     | The run started but did not complete. This state can be entered by stopping the run manually or during preemption                                                                                      |
| Failed      | An error was raised during the execution of the run                                                                                                                                                    |

```{toctree}
:maxdepth: 2
:hidden:

secrets