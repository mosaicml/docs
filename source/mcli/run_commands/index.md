
# Configure a run

Our custom code training product gives you full customization for you to configure and run training jobs, powered by customized YAML files. This section will walk you through how to prepare your system and your YAML file to prepare to train. 

## A quick example

Here is a brief example of a YAML file and the Python SDK used to custom train a model on a dataset.

````{tab-set-code}

```{code-block} yaml
name: hello-composer
image: mosaicml/pytorch:latest
command: 'echo $MESSAGE'
compute:
  cluster: <fill-in-with-cluster-name>
  gpus: 0
scheduling:
  priority: low
integrations:
  - integration_type: git_repo
    git_repo: mosaicml/benchmarks
    git_branch: main
env_variables:
  MESSAGE: "hello composer!"
```

```{code-block} python
from mcli import RunConfig
config = RunConfig(
    name='hello-composer',
    image='mosaicml/pytorch:latest',
    command='echo $MESSAGE',
    compute={'gpus': 0},
    scheduling={'priority': 'low'},
    integrations=[
        {
         'integration_type': 'git_repo',
         'git_repo': 'mosaicml/composer',
         'git_branch': 'main'
        }
    ],
    env_variables={'MESSAGE': 'hello composer!'},
)
```
````

## Configure a custom code training run

Run submissions to the Databricks Mosaic AI training platform can be configured through a YAML file or using our Python API's {class}`~mcli.RunConfig` class. The fields are identical across both methods:

| Field                | Required | Type                                              | Description                                                                                                                                                                                                                           |
| -------------------- | -------- | ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`               | required | `str`                                             | Primary identifier for a run. A unique identifier is automatically appended to the provided name and can be seen in MCLI.                                                                                                             |
| `image`              | required | `str`                                             | Runs execute within [Docker containers](https://docs.docker.com/get-started/overview/#containers) defined by a [Docker image](https://docs.docker.com/get-started/overview/#images).                                                  |
| `command`            | required | `str`                                             | What is actually executed when the run starts. If applicable, this is where you will write your [Composer launch command](https://docs.mosaicml.com/projects/composer/en/latest/trainer/using_the_trainer.html#distributed-training). |
| `compute`            | required | {class}`ComputeConfig`    | Specifies which compute resources to use for your run. More details [below](#managing-compute).                                                                                                                                       |
| `scheduling`         | optional | {class}`SchedulingConfig` | How the scheduler will manage your run.                                                                                                                                                                                               |
| `integrations`       | optional | `List[Dict]`                                      | First class integrations, like Github and MLflow, to customize aspects of run setup and your environment.                                                                                                                             |
| `env_variables`      | optional | `Dict[str, str]`                                  | Additional variables to customize aspects of run setup and your environment.                                                                                                                                                          |
| `parameters`         | optional | `Dict[str, Any]`                                  | Provided parameters mounted as a YAML file of your run at `/mnt/config/parameters.yaml` for your code to access. Used to easily configure your custom training run.                                                                   |
| `metadata`           | optional | `Dict[str, Any]`                                  | Multi-purpose, unstructured field for you to include information about your run for personal categorization.                                                                                                                          |
| `experiment_tracker` | optional | `Dict[Dict]`                                      | Experiment tracker configurations to use for your run. Available trackers are [MLflow and WandB](#experiment-tracking).                                                                                                               |

## Additional information about fields

### Image Field
Images on [DockerHub](https://hub.docker.com) can be configured as `<organization>/<image name>`. While we maintain a set of public docker images for [PyTorch](https://hub.docker.com/r/mosaicml/pytorch), [PyTorch Vision](https://hub.docker.com/r/mosaicml/pytorch_vision), and [Composer](https://hub.docker.com/r/mosaicml/composer) on DockerHub that we encourage you to use and can be access using this `image` field in your YAML file or with Python, to pull from private Docker registries, use the [`docker` secret](../getting_started/secrets.md#docker). 

Note that while we default to DockerHub, custom registries are supported, see [Docker's documentation](https://docs.docker.com/engine/reference/commandline/pull/#pull-from-a-different-registry) and [Docker Secret Page](../getting_started/secrets.md#docker) for more details.

### Compute Fields

The compute field specifies which compute resources to request for your run.
The Databricks Mosaic AI training platform will try to infer which compute resources to use automatically.
Which fields are required depend on which and what type of clusters are available to your organization.
If those resources are not valid or if there are multiple options still available, an error will be raised on run submissions, and the run will not be created.

| Field        | Type        | Details                                                                                               |
| ------------ | ----------- | ----------------------------------------------------------------------------------------------------- |
| `gpus`       | `int`       | Typically required, unless you specify `nodes` or a cpu-only run                                      |
| `cluster`    | `str`       | Required if you have multiple clusters                                                                |
| `gpu_type`   | `str`       | Optional                                                                                              |
| `instance`   | `str`       | Optional. Only needed if the cluster has multiple GPU instances                                       |
| `cpus`       | `int`       | Optional. Typically not used other than for debugging small deployments.                              |
| `nodes`      | `int`       | Optional. Alternative to `gpus` - typically there are 8 GPUs per node                                 |
| `node_names` | 'List[str]` | Optional. Names of the nodes to use in the run. You can find these via `mcli describe cluster <name>` |

You can read more about managing your available compute [here](#managing-compute).

### Scheduling Field

The `scheduling` field governs how the platform's scheduler will manage your run. It is a simple dictionary, currently containing one key: `priority`.

| Field                     |          | Type    | Description                                                                                                                                                                                                         |
| ------------------------- | -------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `priority`                | optional | `str`   | Runs are queued by priority, then by creation time. This parameter defaults to `auto` when omitted or used with unavailable options but can be overridden to `low` or `lowest` to allow other runs higher priority. |
| `preemptible`             | optional | `bool`  | Set to `true` if you would like higher priority jobs to jump this job in the queue.                                                                                                                                 |
| `max_retries`             | optional | `int`   | Maximum number of times our system will attempt to retry your run.                                                                                                                                                  |
| `retry_on_system_failure` | optional | `bool`  | Set to `true` if you would like your run to be retried upon system failure.                                                                                                                                         |
| `max_duration`            | optional | `float` | Time duration, in hours, that your run can run for before it is automatically stopped.                                                                                                                              |


### Integrations Field

We support many [Integrations](integrations.md) to customize aspects of both the run setup and environment. Integrations are specified as a list in your YAML. Each item in the list must specify a valid `integration_type` along with the relevant fields for the requested integration.

Some integrations may require adding secrets. For example, pulling from a private github repository would require the `git-ssh` secret to be configured. See more details on our [Secrets Page](../getting_started/secrets.md).

### Environment Variables Field
Environment variables can be injected into each run at runtime through the `env_variables` field. Databricks Mosaic AI Platform automatically sets certain environment variables and allows you to create your own environment variables. 

#### Automatically Set Environment Variables

We automatically set the following environment variables in your run container.

| Variable            | Description                                                                                              |
| ------------------- | -------------------------------------------------------------------------------------------------------- |
| `MASTER_ADDR`       | The network address of the node with rank 0 in the training job                                          |
| `MASTER_PORT`       | The network port of the node with rank 0 in the training job                                             |
| `NODE_RANK`         | The rank of the node the container is running on, indexed at zero                                        |
| `RUN_NAME`          | The name of your run as seen in the output of `mcli get runs`                                            |
| `COMPOSER_RUN_NAME` | Identical to `RUN_NAME`, used by [composer](https://github.com/mosaicml/composer)                        |
| `WORLD_SIZE`        | The total number of GPUs being used for the training run                                                 |
| `MOSAICML_PLATFORM` | `true` if you are using the Mosaic AI Platform, used by [composer](https://github.com/mosaicml/composer) |
| `PARAMETERS`        | The path that your run parameters are stored in                                                          |
| `RESUMPTION_INDEX`  | The index of the number of times your run has resumed, starting at zero                                  |
| `NUM_NODES`         | The total number of nodes the run is scheduled on                                                        |
| `LOCAL_WORLD_SIZE`  | The number of GPUs available to the run on each node                                                     |

#### Create your own Environment Variables
To add non-sensitive environment variables, use the `env_variables` field in your YAML:

```yaml
name: using-env-variables
image: bash
env_variables:
  FOO: 'Hello World!'
command: |
  echo "$FOO"
```

### Experiment tracking

We support both MLflow and WandB as experiment trackers to monitor and visualize the metrics for your training runs. Set `experiment_tracker` to contain the configuration for the tracker you want to use. 

#### MLflow

Provide the full path for the experiment, including the experiment name. In Databricks Managed MLflow, this will be a workspace path resembling
`/Users/example@domain.com/my_experiment`. You can also provide a `model_registry_path` for model deployment. Make sure to configure your [Databricks secret](../getting_started/secrets.md#databricks).

```{code-block} yaml
experiment_tracker:
  mlflow:
    experiment_path: /Users/example@domain.com/my_experiment
    model_registry_path: catalog.schema | catalog.schema.model_name # optional
```


#### Weights & Biases
Include both project name and entity name in your configuration, and make sure to set up your [WandB secret](../getting_started/secrets.md#weights--biases).

```{code-block} yaml
experiment_tracker:
  wandb:
    project: my-project
    entity: my-entity
```

### Metadata Field

Metadata is meant to be a multi-purposed, unstructured place to put information about a run.
It can be set at the beginning of the run, for example to add custom run-level tags or groupings:

```yaml
name: hello-world
image: bash
command: echo 'hello world'
metadata:
  run_type: test
```

Metadata on your run is readable through the CLI or SDK:

````{tab-set-code}

```{code-block} bash
> mcli describe run hello-world-VC5nFs
Run Details
Run Name      hello-world-VC5nFs
Image         bash
...
Run Metadata
KEY         VALUE
run_type    test
```

```{code-block} python
from mcli import get_run

run = get_run('hello-world-VC5nFs')
print(run.metadata)
# {"run_type": "test"}
```
````

You can also update metadata when the run is running, which can be helpful for exporting metrics or information from the run:

```python
from mcli import update_run_metadata

run = update_run_metadata("hello-world-VC5nFs", {"run_type": "test_but_updated"})
print("New metadata values:", run.metadata)
```

```{admonition} Metadata size constraints
Metadata is not intended for large amounts of data such as time series data. Each key is limited to 200 characters and value is limited to 0.1mb. Metadata cannot have more than 200 keys. A {class}`~mcli.MAPIException` will be raised on creation or updates if any of these limits are exceeded.
```

## Managing Compute
The Databricks Mosaic AI platform configures and manages clusters for you automatically.

To view clusters you have access to:

```bash
mcli get clusters
```

View current cluster utilization for all available clusters:

```bash
mcli util
```

Or view current cluster utilization for a specific cluster:

```bash
mcli util {cluster_name}
```

View specific cluster details:

```bash
mcli describe cluster {cluster_name}
```

### Using compute resources

When submitting a run or deployment on a cluster, the Databricks Mosaic AI training platform will try to infer which compute resources to use automatically.
Which fields are required depend on which and what type of clusters are available to you or your organization.
If those resources are not valid or if there are multiple options still available, an error will be raised on run submissions, and the run will not be created.

| Field      | Type  | Details                                                               |
| ---------- | ----- | --------------------------------------------------------------------- |
| `gpus`     | `int` | Typically required, unless you specify `nodes` or a cpu-only run      |
| `cluster`  | `str` | Required if you have multiple clusters                                |
| `gpu_type` | `str` | Optional                                                              |
| `instance` | `str` | Optional. Only needed if the cluster has multiple GPU instances       |
| `nodes`    | `int` | Optional. Alternative to `gpus` - typically there are 8 GPUs per node |
| `cpus`     | `int` | Typically not used other than for debugging small deployments.                                     
| `node_names` | 'List[str]` | Optional. Names of the nodes to use in the run. You can find these via `mcli describe cluster <name>` |                          |

For example, you can launch a multi-node cluster `my-cluster` with 16 A100-80 GPUs:

```yaml
compute:
  cluster: my-cluster
  gpus: 16
  gpu_type: a100_80gb
```

Most compute fields are also optional CLI arguments.

```{toctree}
:maxdepth: 2
:hidden:

integrations