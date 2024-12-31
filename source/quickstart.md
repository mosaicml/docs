# Quickstart

Welcome to Databricks Mosaic AI Training! With just a few simple steps, get started training and deploying your models.

First, install [MCLI](https://mcli.docs.mosaicml.com), the command line interface to Mosaic AI Training, via `pip` into your python3 environment:

```bash
pip install --upgrade mosaicml-cli
```

Register your API key by following the instructions in this command:

```bash
mcli init
```

To manually manage your account and create API keys, visit the [Mosaic AI console](https://console.mosaicml.com). This API key can be reset in mcli by using:

```bash
mcli set api-key <value>
```

You can also skip this step and use the environment variable `MOSAICML_API_KEY` to automatically configure access.

## Run "Hello World" 🌎

To submit your first run, copy the below yaml into a file called 'hello_world.yaml':

```yaml
name: hello-world
gpu_num: 0
image: bash
command: |
  sleep 2
  echo Hello World!
```

Then, run:

```bash
mcli run -f hello_world.yaml --follow
```

If you see "Hello World!", congratulations on setting up MCLI!
Follow the documentation for next steps:

- Learn [how to configure and customize training runs](https://docs.mosaicml.com/projects/mcli/en/latest/training/yaml_schema.html)
- Add integrations with [github, docker, cloud storage, and experiment trackers](https://docs.mosaicml.com/projects/mcli/en/latest/resources/integrations/index.html)
- Train your first [1 billion parameter GPT model](https://docs.mosaicml.com/projects/mcli/en/latest/guides/first_llm.html)
- Explore [what happens at each phase of the run lifecycle](https://docs.mosaicml.com/projects/mcli/en/latest/training/run_lifecycle.html)