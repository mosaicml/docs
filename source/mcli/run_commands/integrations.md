
# Integrations

**Integrations** span across clusters, secrets, environment variables and how an execution environment is created.
They provide easy ways to configure the execution environment of your runs and properly set up dependencies.
For example, a [Weights and Biases](https://wandb.ai) integration may uniquely identify a run and surface links to easily find the run within W&B (while handling the project, organization, and run naming for you).

## How to Specify Integrations

Integrations are specified as a list in the MCLI YAML.
Each integration in the list specifies a valid `integration_type` (see below for supported types) along with any parameters relevant to that integration type as shown below:

```yaml
integrations:
  - integration_type: <insert_integration_type>
    <integration_param>: <integration_value>
```

For example:

```yaml
integrations:
  - integration_type: "git_repo"
    git_repo: mosaicml/composer
    git_branch: v0.7.1
    pip_install: .
  - integration_type: "apt_packages"
    packages:
      - htop
  - integration_type: "pip_packages"
    packages:
      - numpy
  - integration_type: "wandb"
    project: ben_bitdiddle_llms
    entity: mosaicml
```


## Available Integrations
Each `integration_type` has different available parameters that configure how it affects your run environment.
For information on each specific integration type, visit the page for that integration.
* [APT Packages](#apt-packages)
* [Comet](#cometml)
* [Github](#github)
* [MLflow](#mlflow)
* [PyPi Packages](#pypi-packages)
* [Weights & Biases](#weights-and-biases)

### APT Packages

The APT Packages integration installs APT packages in your run execution environment.

In order to include the APT packages integration, use `integration_type: apt_packages`.

#### Required Parameters

The only required parameter (and the only parameter overall) for APT Packages is `packages` field,
which corresponds to a list of all apt packages to install.

Note that you can include package version constraints along with the package name just as you would in a `apt install` command.

#### Example

```yaml
integrations:
  - integration_type: apt_packages
    packages:
      - htop=3.2.0
      - python3-dev
```

### CometML

The [CometML](https://comet.com) (comet_ml) integration automatically sets the relevant environment variables that Comet relies on in the run execution environment.

```{admonition} CometML Logger must be configured in Composer
This integration only sets up the environment, the logger itself must still be configured in Composer. See Composer's [Logging](https://docs.mosaicml.com/projects/composer/en/latest/trainer/logging.html) and [CometMLLogger](https://docs.mosaicml.com/projects/composer/en/latest/api_reference/generated/composer.loggers.CometMLLogger.html).
```

Note that the **run name** for the Comet run will default to the `name` of the MCLI run,
unless another `name` is passed into Composer's [CometMLLogger](https://docs.mosaicml.com/projects/composer/en/latest/api_reference/generated/composer.loggers.CometMLLogger.html) in which case that will take precedence.

In order to include the comet_ml integration, use `integration_type: comet_ml`.

#### Setup: CometML API Key

This integration requires providing your Comet API key to the Databricks Mosaic AI platform.
Retrieve or generate your Comet API Key at this [link](https://www.comet.com/account-settings/apiKeys), then create an environment variable secret:

```bash
mcli create secret env COMET_API_KEY=<YOUR COMET API KEY>
```

This command creates a secret which will mount your API key in the run execution environment as the variable
`COMET_API_KEY`.
For more details on how this works, see the [Environment Secrets Page](../getting_started/secrets.md#environment-variable)

#### Required Parameters

The `comet_ml` integration has no required parameters.
However, if no parameters are specified then there won't be any configuration set for CometML.

#### Optional Parameters

Optional parameters of the CometML Integration are used to configure the CometML logger.

Optional parameters include: `project`, `workspace`.

- `project` (str): The CometML project to log to. `Default: None`
- `workspace` (str): The organization the CometML user belongs to. `Default: None`.

```{admonition} Always Set project and workspace
Even though all comet_ml parameters are optional, we **strongly recommend always setting project and workspace** for all your runs
so that they appear in an expected place in your CometML account.
```

#### Example

```yaml
integrations:
  - integration_type: comet_ml

    # The comet_ml project (we recommend you always specify a project)
    project: my_project

    # The account to log to (we recommend you always specify an workspace)
    workspace: mosaic-ml
```



### Github

The git repo integration **clones a git repo into the working directory of your run's execution environment** comes
with a number of configurable options (see below) for the cloning and setup of the repo.

In order to include the git repo integration, use `integration_type: git_repo`. Note that you can have any number of these
included in your YAML.

#### Prerequisite: Git SSH Secret Setup

In order to clone from private repositories you will have to set up an SSH key that gives the MosiacML platform clone access to the repo.
Follow the steps for **creating a `git-ssh` secret on the [SSH Secrets Page](../getting_started/secrets.md#github) to set up a git SSH secret.**

#### Required Parameters

The only required parameter in the Git Repos integration is the `git_repo` field, which corresponds to the
repo name in <organization>/<repo> format.

```yaml
integrations:
  - integration_type: git_repo
    git_repo: mosaicml/composer
```

#### Optional Parameters

Optional parameters of the Git Repos Integration configure how the repo is cloned and installed.

Optional parameters include: `git_branch`, `git_commit`, `path`, `ssh_clone`, `pip_install` and `host`.

`git_branch` (str): Clone the repo with a specific branch checked out. `Default: the repo default branch`.

`git_commit` (str): Commit your changes in git.

`path` (str): Clone the repo to a specific path inside of the image. ( Note: by default git clones to the repo name within the image's working directory, e.g. `composer` if `git_repo` is `mosaicml/composer`). Specifying this value is equivalent to runing
`git clone <repo url> <path>`. `Default: the repo name`.

`ssh_clone` (bool): Use SSH keys to clone the git repo. To use HTTPS, `ssh_clone=False`. `Default: true`.

`host` (str): The hostname for the git repo. `Default: github.com`.

```{admonition} Git SSH Secret
Note that to properly clone private repos with SSH you will need an [Github SSH Secret](../getting_started/secrets.md#github) set.
```

`pip_install` (str): Pip install the cloned repo. The value of this field is used in `pip install <value>`.
`Default: no pip install`.

#### Example

```yaml
integrations:
  - integration_type: git_repo

    # github.com/mosaicml/composer
    git_repo: mosaicml/composer

    # The git branch to checkout (optional, default = the repo default branch)
    git_branch: my-branch

    # Clone to /workspace/composer (optional, default = the repo name)
    path: /workspace/my_composer_clone

    # Use SSH Keys to clone (optional, default = True)
    ssh_clone: True

    # pip install command for the repo (optional, default = None)
    pip_install: -e .[all]

    # host for the git repo (defaults to github.com)
    host: github.com
```

The above settings are equivalent to:

```bash
> git clone git@github.com:mosaicml/composer.git -b my-branch /workspace/my_composer_clone
> cd my_composer_clone
> pip install -e .[all]
> cd ..
```

#### Example: Multi-Repo Install

One common use case for the Git repo integration is to clone multiple repos in the same environment.

To do this, it is as easy as just adding multiple git integrations.

```yaml
integrations:
  - integration_type: git_repo
    git_repo: mosaicml/composer
    path: /workspace/composer
    git_branch: v0.8.1
    pip_install: -e .[all]
  - integration_type: git_repo
    git_repo: facebookresearch/xformers
    path: /workspace/xformers
    pip_install: -e .
  - integration_type: git_repo
    git_repo: myuser/privaterepo
    path: /workspace/myrepo
```

In the above example, we are cloning and adding three different repos with different instructions.
Because we set the filepaths specifically with the Git Integration `path` option, the resulting filestructure looks like:

```
workspace
├── composer
├── myrepo
└── xformers
```

where `workspace` is the working directory of the container being used for the run.

```{admonition} Checking Out Branches
Note that the mosaicml/composer repo is checked out of `v0.8.1` and installed from the `v0.8.1` branch with the pip installation options `pip install -e .[all]`
```


### MLflow

The MLflow integration automatically sets the relevant environment variables that MLflow relies on in the run execution environment.

```{admonition} MLflow Logger must be configured in Composer
This integration only sets up the environment, the logger itself must still be configured in Composer. See Composer's [Logging](https://docs.mosaicml.com/projects/composer/en/latest/trainer/logging.html) and [MLFlowLogger](https://docs.mosaicml.com/projects/composer/en/latest/api_reference/generated/composer.loggers.MLFlowLogger.html).
```

#### Using MLflow in a run (managed through Databricks)

This section will explain how to use MLflow for a run. To use this integration, set up your credentials with the [`databricks` secret](../getting_started/secrets.md#databricks).
To use MLflow experiment tracking in a run, include the MLflow integration in your run config:

````{tab-set-code}

```{code-block} yaml
integrations:
  - integration_type: mlflow
    experiment_name: /Users/example@domain.com/my_experiment
```

```{code-block} python
from mcli import RunConfig
config = RunConfig(
    ...
    integrations=[
        {
         'integration_type': 'mlflow',
         'experiment_name': '/Users/example@domain.com/my_experiment',
        }
    ],
)
```
````

- `experiment_name` (str, required): The name to use for the experiment. Databricks MLflow users see [this page](https://docs.databricks.com/en/mlflow/experiments.html) for more information about experiment and workspace organization (example Databricks experiment name: `/Users/<email>/<experiment_name>`).
- `tracking_uri` (str, optional): Default is `databricks` , e.g. managed MLflow through Databricks

<details>
  <summary>Using MLflow in a run (unmanaged)</summary>

You do not have to have a Databricks managed MLflow account to use MLflow, however your run will be responsible for uploading the MLflow artifacts before the run terminates. 
See the [MLflow documentation](https://mlflow.org/docs/latest/tracking.html) for options

````{tab-set-code}

```{code-block} yaml
integrations:
  - integration_type: mlflow
    experiment_name: my_experiment
    # See MLflow docs for all tracking_uri alternatives
    tracking_uri: file:/my/local/dir
```

```{code-block} python
from mcli import RunConfig
config = RunConfig(
    ...
    integrations=[
        {
         'integration_type': 'mlflow',
         'experiment_name': 'my_experiment',
         'tracking_uri': 'file:/my/local/dir',  # See MLflow docs for all alternatives
        }
    ],
)
```
````


</details>

### PyPI Packages

The PyPI Packages integration installs Python packages in your run execution environment.

In order to include the PyPI integration, use `integration_type: pip_packages`.

#### Required Parameters

The only required parameter (and the only parameter overall) for this integration is the `packages` field, which corresponds to a list of all packages to install.

Note that you can include package version constraints along with the package name just as you would in a `pip install` command.

#### Optional parameters

The only optional parameter is the `upgrade` parameter which when set to `true` adds a `--upgrade` to the `pip install` command and when set to `false` does not. For more details on how `upgrade` works, see the [pip documentation](https://pip.pypa.io/en/stable/cli/pip_install/#cmdoption-U).

Note that if `upgrade` is set to `true` then it will be used for all pip packages being installed.
## Example

```yaml
integrations:
  - integration_type: pip_packages
    packages:
      - wheel
      - xformers==4.20.0
      - requests>=2.27.1
    upgrade: true
```



### Weights and Biases

The [Weights and Biases](https://wandb.ai) (WandB) integration automatically sets the
relevant environment variables that WandB relies on in the run execution environment.

```{admonition} WandB Logger must be configured in Composer
This integration only sets up the environment, the logger itself must still be configured in Composer. See Composer's [Logging](https://docs.mosaicml.com/projects/composer/en/latest/trainer/logging.html) and [WandBLogger](https://docs.mosaicml.com/projects/composer/en/latest/api_reference/generated/composer.loggers.WandBLogger.html#composer.loggers.WandBLogger).
```

Note that the **run name** for the WandB run will default to the `name` of the MCLI run,
unless another `name` is passed into Composer's [WandBLogger](https://docs.mosaicml.com/projects/composer/en/latest/api_reference/generated/composer.loggers.WandBLogger.html#composer.loggers.WandBLogger), in which case that will take precedence.

#### First Time Setup: WandB API Key

This integration requires providing your WandB API key to the Databricks Mosaic AI platform.
Generate an WandB API Key at this [link](https://wandb.ai/settings), then create an environment variable secret:

```bash
mcli create secret env WANDB_API_KEY=<YOUR WANDB API KEY>
```

This command creates a secret which will mount your API key in the run execution environment as the variable
`WANDB_API_KEY`.
For more details on how this works, see the [Environment Secrets Page](../getting_started/secrets.md#environment-variable).

#### Using Weights and Biases in a Run

To use WandB experimenting tracking in a run, include the WandB integration in the YAML:

```yaml
integrations:
  - integration_type: wandb

    # The Weights and Biases project name
    project: my_project

    # The username or organization the Weights and Biases project belongs to
    entity: mosaic-ml
```

Required parameters include: `project`, `entity`:

- `project` (str): The WandB [project name](https://docs.wandb.ai/ref/app/pages/project-page)
- `entity` (str): An entity is a username or team name where you're logging runs. This entity must exist before you can use it, so make sure it is configured first in the [WandB UI](https://wandb.ai)

#### Optional Parameters

Optional parameters of the Weights and Biases Integration are used to configure the Weights and Biases logger.

Optional parameters include: `group`, `job_type`, `tags`:

- `group` (str): The group the run belongs to. For more information on grouping runs see
  [the Weights and Biases docs](https://docs.wandb.ai/guides/track/advanced/grouping). `Default: None`.
- `job_type` (str): The Weights and Biases job type. This is useful when you're grouping runs together into larger experiments using groups (e.g. "train", "eval"). `Default: None`.
- `tags` (List[str]): A list of tags for the run. Tags are useful for organizing runs together (e.g. "baseline", "production"). `Default: []`.

#### Example

```yaml
integrations:
  - integration_type: wandb

    # The Weights and Biases project name
    project: my_project

    # The organization the Weights and Biases user belongs to
    entity: mosaic-ml

    # Make the run a member of this run group
    group: my_sweep

    # A job type to tag the run with
    job_type: train

    # Tags for the run
    tags:
      - first_tag
      - second_tag
```
