# Run commands

Runs can be managed using MCLI. 
Below outlines how to work with runs, including creation, following, getting, stopping, and deleting runs.
All CLI commands come with a `--help` flag that includes detailed instructions on arguments needed and additional options

## Submitting a run

| CLI Command | Description |
| ----------- | ----------- |
| `mcli run -f <yaml>` | Submit a custom code training run with the provided configuration |
| `mcli run --clone <name>` | Submit a new custom code training run using an existing run's configuration |
| `mcli run -r <name>` | Resubmit and restart an existing run that has since terminated |
| `mcli interactive --hours 5` | Create an interactive run for local development |

## Managing a run

| CLI Command | Description |
| ----------- | ----------- |
| `mcli get runs` | List the last 50 runs you have submitted |
| `mcli get runs --user name@email.com` | List all runs for a user in your organization. Works only if "Shared runs" are enabled |
| `mcli describe run <name>` | Get detailed information about a run, including the config that was used and run events |
| `mcli logs <name>` | Retrieve the latest console log of the indicated run |
| `mcli logs <name> --resumption <N>` | Retrieve the console log for a given resumption of the indicated run |
| `mcli stop run <name>` | Stop the provided run |
| `mcli delete run <name>` | Delete the run and its associated logs from the cluster |
| `mcli update run <name>` | Update run scheduling parameters, like the max time that a run can run for |
| `mcli watchdog <name>` | Turn on [`Watchdog`](#enabling-watchdog) for automatic retries |
| `mcli diff run <name> <name>` | Compare the configuration of two runs |
| `mcli connect <name>` | Connect to the container of any running run |

## Enabling Watchdog
When training large models across many nodes, inevitably some nodes may fail over time due to hardware issues
halting any in-progress training runs. Instead of manually restarting these runs, enabling Watchdog either in 
your YAML file or via MCLI for every run you submit will automatically restart the run if system or node failure 
is detected. 

To enable Watchdog via MCLI, use:

```bash
mcli watchdog <run_name>
```

To disable Watchdog via MCLI, use:

```bash
mcli watchdog --disable <run_name>
```

You can also configure Watchdog on run submission via your run YAML by specifying the following fields in your scheduling parameter:

```yaml
scheduling:
  retry_on_system_failure: True
  max_retries: 10
```

If Watchdog is enabled for your run, you'll see a 🐕 icon next to your `run_name` in the `mcli get runs` display.
By default, enabling Watchdog will automatically retry your run `10` times.
You can configure this default in your yaml by overriding the `max_retries` [scheduling parameter](../run_commands/index.md)

### Graceful resumption from a checkpoint using LLM Foundry and Composer
Watchdog restarts the run from the beginning; it does not handle graceful resumption from a checkpoint automatically. To handle these resumptions gracefully, use Watchdog with LLM Foundry or Composer, or include customized logic in your command to resume from a specified checkpoint.

**Via LLM Foundry**
For more efficient training with Watchdog, you can configure autoresume from a checkpoint using [LLM Foundry training](https://github.com/mosaicml/llm-foundry/tree/main/scripts/train)
by passing in a configured `save_folder` inside your parameters.


**Via Composer**
For more efficient training with Watchdog, you can configure autoresume from a checkpoint using Composer. To do so, pass both of the below
arguments into the [Composer Trainer](https://docs.mosaicml.com/projects/composer/en/stable/trainer/using_the_trainer.html):

- `autoresume`: Should be set to `True` to resume from latest checkpoint
- `save_folder`: The remote folder where checkpoints should be saved during training. Checkpoints are written to this folder at the `save_interval` interval. If a run crashes between checkpoints, auto-resume will pick up at the latest checkpoint

A full end-to-end example is available in the [Composer Autoresume documentation](https://docs.mosaicml.com/projects/composer/en/stable/examples/checkpoint_autoresume.html)

## Interactive Mode

Interactive runs give the ability to debug and iterate quickly inside your cluster in a secure way. Interactivity works on top of the existing MosaicML runs, so before connecting a run workload needs to be submitted to the cluster. For security purposes storage is not persisted, so we recommend using your own cloud storage and git repositories to stream and save data between runs.

More details can be found on our [Interactive Runs](https://docs.mosaicml.com/projects/mcli/en/latest/training/interactive.html) page. 

## Dependent Deployments

Dependent Deployments is a framework that allows you to configure a sidecar image inside a training run. This can be useful for tasks such as batch inference or evaluation that require an inference engine for efficient generation and orchestrating large amounts of GPUs. Read our [Dependent Deployments](https://docs.mosaicml.com/projects/mcli/en/latest/training/depdeps.html) documentation for more information. 

```{toctree}
:maxdepth: 2
:hidden:

interactive