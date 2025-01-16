# Secrets

Secrets allow you to inject sensitive values into your runs, such as API keys, passwords, or other access keys. These can be used to access your personal accounts for the various integrations we support. Secrets can be configured as an environment variable or through a mounted file, and are automatically available to every run, across clusters. Secrets are set by users and cannot be shared across users. Secrets can be listed using MCLI:

```bash
> mcli get secrets
NAME  TYPE
example     environment
example2    environment
example3    ssh
```

## Environment Variable

Secrets can be surfaced as environment variables using the `env` secret type. These environment variables are injected at runtime. To create a secret as an environment variable, run:

```bash
mcli create secret env NAME=my-super-secret
```

```
✔  Created environment secret: name
✔  Synced to all clusters
```

The above secret can then be accessed during your run as the environment variable `NAME` and value `my-super-secret`. To verify the secret was properly created:

```bash
> mcli get secrets
NAME  TYPE
example     environment
example2    environment
example3    ssh
```

As with all other secrets, `env` secrets will be injected into every one of your subsequent runs. If you are looking to inject non-sensitive environment variables into individual runs, specify them in your [run configuration](../run_commands/index.md)


## Mounted File

You can securely add arbitrary confidential information to your workloads by using file-mounted secrets.
To create a file-mounted secret, use the `mounted` secret type:

```bash
> mcli create secret mounted
? What would you like to name this secret? mounted-secret
? What data would you like to store? ****************
✔  Created secret: mounted-secret
```

This command will request the secret name and confidential data you wish to store.
By default, the secret will be mounted at the path `/secrets/<secret-name>/secret` (`/secrets/mounted-secret/secret` above). This mount path can be changed by supplying the `--mount-path` argument.

The path will be made available as the environment variable `$SECRET_PATH_<UPPER_NAME>`, where `<UPPER_NAME>` is the secret name, all upper-case with "-" replaced by "\_".

Once you've added your file-mounted secret, you can verify that it exists by running the following YAML:

```yaml
name: check-file
image: bash
command: |
  ls -l $SECRET_PATH_MOUNTED_SECRET
```

Save this YAML locally as `check-file.yaml` and run it with `mcli run -f check-file.yaml`.
You should see the following:

```bash
> mcli run -f check-file.yaml

i  Run check-file-6khr submitted. Waiting for it to start...
i  You can press Ctrl+C to quit and follow your run manually.
✔  Run check-file started
i  Following run logs. Press Ctrl+C to quit.

lrwxrwxrwx    1 root     root            13 Jun 21 23:15 /secrets/mounted-secret/secret -> ..data/secret
```

### Deleting & Modifying Secrets

Secrets by design are not modifiable. To edit the existing secret, delete the secret first and then re-create:

```bash
mcli delete secret secret-stuff
mcli create secret env SECRET_STUFF='super-secret-name2'
```

### Automatically mounted secrets

Access to the Databricks Mosaic AI platform inside your run is automatically configured with your user's permissions. 
You can use this to interact with the platform via the CLI or SDK.
For example, you can launch a run inside a run or make updates to the existing run.

## Available Secrets
* [Cloudflare R2](#cloudflare-r2)
* [CoreWeave Object Store](#coreweave-object-store)
* [Databricks](#databricks)
* [Docker](#docker)
* [GCP Storage](#gcp-storage)
* [Github](#github)
* [Huggingface](#huggingface)
* [OCI](#oci)
* [S3](#aws-s3)
* [SSH Keys](#ssh-keys)
* [Weights & Biases](#weights--biases)

### Cloudflare R2
Cloudflare r2 is an [s3-compatible](https://developers.cloudflare.com/r2/api/s3/api/) storage system. Developers can perform many CRUD operations on r2 with AWS CLIs and SDKs. In practice, a Cloudflare integration feels very much like an S3 integration.

Retrieve your R2 **Secret Access Key** and **Access Key ID** key-pair. If you do not have one then follow the instructions [here](https://developers.cloudflare.com/r2/api/s3/tokens/) to create a key-pair. 

Store the information above in a credentials file (ie `~/.r2/credentials`):

```bash
[default]
aws_access_key_id=<your_cloudflare_access_key_id>
aws_secret_access_key=<your_cloudflare_access_secret_key>
```

Create an empty config file (ie `~/.r2/config`) as:
```bash
[default]
```

Find your Cloudflare accountID using [these instructions](https://developers.cloudflare.com/fundamentals/get-started/basic-tasks/find-account-and-zone-ids/). Use the account ID to set a Databricks Mosiac AI Platform environment variable secret:

```bash
mcli create secret env S3_ENDPOINT_URL='https://{ACCOUNT_ID}.r2.cloudflarestorage.com' 
```

Now we can treat these credentials as if they are for AWS S3. Run the following command: 

```bash
> mcli create secret s3
? What would you like to name this secret? my-r2-credentials
? Where is your S3 config file located? ~/.r2/config
? Where is your S3 credentials file located? ~/.r2/credentials
✔  Created secret: my-r2-credentials
```

The values for each of these queries can also be passed as arguments using the `--name`, `--config-file` and `--credentials-file` arguments, respectively.

Once you’ve created an S3 secret, we mount these secrets inside all of your runs and export two environment variables:
* `$AWS_CONFIG_FILE`: Path to your config file
* `$AWS_SHARED_CREDENTIALS_FILE`: Path to your credentials file

A library like boto3 uses these environment variables by default to discover your s3 credentials:
```python
import boto3
import os

# boto3 automatically pulls from $AWS_CONFIG_FILE and $AWS_SHARED_CREDENTIALS_FILE
s3 = boto3.client('s3', endpoint_url=os.environ['S3_ENDPOINT_URL'])
```

### CoreWeave Object Store

CoreWeave uses an [s3-compatible](https://docs.coreweave.com/docs/products/storage) storage system. This allows developers to CRUD from their CoreWeave blob stores with AWS CLIs and SDKs. In practice, a CoreWeave integration feels very much like an s3 integration.

First, follow [these instructions](https://docs.coreweave.com/docs/products/storage/object-storage/how-to/manage-api-access-tokens) to create a token 
configuration file. The file should look like this:

```bash
[default]
access_key = <your_coreweave_access_key>
secret_key = <your_coreweave_secret_key>
# The region for the host_bucket and host_base must be the same.
host_base = object.lga1.coreweave.com # instead of lga1 it could also be ord1 or las1.
host_bucket = %(bucket)s.object.lga1.coreweave.com
check_ssl_certificate = True
check_ssl_hostname = True
```

Take your `access_key` and `secret_key` from your token configuration file to create a credentials file in `~/.coreweave/credentials`.
The credentials file should look like this:

```bash
[default]
aws_access_key_id=<your_coreweave_access_key>
aws_secret_access_key=<your_coreweave_secret_key>
```

Create an empty config file in `~/.coreweave/config` as:
```bash
[default]
```

Next, create an environment variable for the endpoint url using the `host_base` from your CoreWeave token configuration file:

```bash
mcli create secret env S3_ENDPOINT_URL='https://object.lga1.coreweave.com' #  insead of lga1 it could also be ord1 or las1.
```

Now we can treat these credentials as if they are for aws s3. Run the following command: 

```bash
> mcli create secret s3
? What would you like to name this secret? my-coreweave-credentials
? Where is your S3 config file located? ~/.coreweave/config
? Where is your S3 credentials file located? ~/.coreweave/credentials
✔  Created secret: my-coreweave-credentials
```

The values for each of these queries can be also passed as arguments using the `--name`, `--config-file` and `--credentials-file` arguments, respectively.

Once you’ve created an S3 secret, we mount these secrets inside all of your runs and export two environment variables:
* `$AWS_CONFIG_FILE`: Path to your config file
* `$AWS_SHARED_CREDENTIALS_FILE`: Path to your credentials file

A library like boto3 uses these environment variables by default to discover your s3 credentials:
```python
import boto3
import os

# boto3 automatically pulls from $AWS_CONFIG_FILE and $AWS_SHARED_CREDENTIALS_FILE
s3 = boto3.client('s3', endpoint_url=os.environ['S3_ENDPOINT_URL'])
```

### Databricks

To set up your Databricks credentials, use the `databricks` secret:

```bash
mcli create secret databricks
```

This secret requires providing your workspace URL and Databricks Personal Access Token (PAT) to the Databricks Mosaic AI platform as `host` and `token`, respectively.

`host`: Your Databricks workspace URL. More information on workspace URLs can be found in [this documentation](https://docs.databricks.com/en/workspace/workspace-details.html#workspace-url).

`token`: Generate a Databricks PAT following the instructions [here](https://docs.databricks.com/en/dev-tools/auth.html).

Instead of using the interactive prompt above, all the settings can also be provided as flags in one command:

```bash
mcli create secret databricks --host my-host --token my-token
```

#### Testing your Credentials

To test your Databricks credentials, create a `databricks_secret_check.yaml` with the following run config:

```yaml
name: databricks-secret-check
image: homebrew/brew
compute:
  gpus: 0
command: |
  brew tap databricks/tap
  brew install databricks
  echo "[DEFAULT]
  host  = $DATABRICKS_HOST
  token = $DATABRICKS_TOKEN" >> ~/.databrickscfg
  printf "\n\n\n\n\n========================================\nDatabricks current user info:\n"
  databricks current-user me
```

```bash
mcli run -f databricks_secret_check.yaml --follow
```

If successful, the following will render at the bottom of the output:

```bash
========================================
Databricks current user info:
{
  "active":true,
  "displayName":string,
  "emails": [
    {
      "primary":true,
      "type":string,
      "value":string
    }
  ],
  "groups": [
    {
      "display":string,
      "$ref":string,
      "type":string,
      "value":string
    }
  ],
  "id":string,
  "name": {
    "givenName":string
  },
  "userName":string
}
```

(mcli/getting_started/secrets:docker)=
### Docker

While we maintain a set of public docker images for [PyTorch](https://hub.docker.com/r/mosaicml/pytorch), [PyTorch Vision](https://hub.docker.com/r/mosaicml/pytorch_vision), and [Composer](https://hub.docker.com/r/mosaicml/composer) on DockerHub that we encourage you to use and can be access using the `image` field in your YAML file or with Python, to pull from private Docker registries, use the `docker` secret:

```bash
mcli create secret docker
```

To create this secret, you'll need the server address, your username, and your registry access token. The default server is DockerHub (https://index.docker.io/v1/), but we support custom docker registries. We strongly recommend using API tokens to authenticate. For DockerHub, create an access token [here](https://hub.docker.com/settings/security?generateToken=true).

Instead of using the interactive prompt above, all the settings can also be provided as flags in one command:

```bash
mcli create secret docker --username my-user --password my-registry-key --server https://custom-registry.com
```

#### Testing your Credentials

To test your docker credentials, place the private image name into the following run configuration:

```yaml
name: hello-world
compute:
  gpus: 0
image: <my-private-image>
command: |
  sleep 2
  echo Hello World!
```

```bash
mcli run -f hello-world.yaml
```

If successful, the following will render at the bottom of the output:

```
> mcli run -f hello-world.yaml

i  Run hello-world-po9z submitted. Waiting for it to start...
i  You can press Ctrl+C to quit and follow your run manually.
✔  Run hello-world started
i  Following run logs. Press Ctrl+C to quit.

Hello World!
```

If, however, your secret has not been set up properly you'll see:

```
> mcli run -f hello-world.yaml

------------------------------------------------------
Let's run this run
------------------------------------------------------

i  Run hello-world-61lx submitted. Waiting for it to start...
i  You can press Ctrl+C to quit and follow your run manually.
✗  Run hello-world-61lx failed to start and will be deleted because it could still be consuming resources.
    Could not find Docker image "<my-private-image>". If this is a private image, check `mcli get secret --type docker_registry` to ensure that you have the Docker secret created. If not, create one using `mcli create secret docker`. Otherwise, double-check your image name.
```

When starting runs, the image can also be overridden at the command line:

```bash
mcli run -f hello-world.yaml --image <new-image>
```


### GCP Storage

In order to stream data from GCP storage buckets when training models, MCLI will need access to your GCP credentials.

There are two ways to add accessible GCP credentials to MCLI.

#### GCP Service Account Credentials

The first way is to create a service account key to your associated GCP bucket and provide the associated JSON credentials to MCLI. For instructions, see the link [here](https://cloud.google.com/iam/docs/creating-managing-service-account-keys). This will allow you to immediately access your bucket via the [`google-cloud-storage`](https://pypi.org/project/google-cloud-storage/) client within your code. To add GCP credentials to MCLI this way, use the following command:

```bash
mcli create secret gcp
```

which produces the following output:

```bash
> mcli create secret gcp
? What would you like to name this secret? my-gcp-credentials
? Where is your gcp credentials file located? <my_gcp_credentials.json>
✔  Created secret: my-gcp-credentials
```

The values for each of these queries can be passed as arguments using the --name and --credentials-file arguments, respectively. Your [credentials file](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) should follow the standard structure output as referenced by the google cloud documentation:

```json
{
  "type": "service_account",
  "project_id": "<PROJECT_ID>",
  "private_key_id": "<KEY_ID>",
  "private_key": "-----BEGIN PRIVATE KEY-----\n<PRIVATE_KEY>\n-----END PRIVATE KEY-----\n",  // gitleaks:allow
  "client_email": "<SERVICE_ACCOUNT_EMAIL>",
  "client_id": "<CLIENT_ID>",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://accounts.google.com/o/oauth2/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/<SERVICE_ACCOUNT_EMAIL>"
}
```

Once you’ve created a GCP secret, the credentials file will be mounted inside all of your runs.
We set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` automatically, so that libraries like [`google-cloud-storage`](https://pypi.org/project/google-cloud-storage/) can automatically detect the credentials:

```python
from google.cloud import storage

storage_client = storage.Client()
buckets = list(storage_client.list_buckets())
print("my buckets: ", buckets)
```

#### GCP User Auth Credentials Mounted as Environment Variables

The second way to add your [GCP user credentials](https://cloud.google.com/storage/docs/authentication) or [HMAC key](https://cloud.google.com/storage/docs/authentication/hmackeys) is to set your GCP user access key and GCP user access secret as environment variables for your runs. You can set these environment variables as such.

```bash
mcli create secret env GCS_KEY=<GCS_KEY value>
mcli create secret env GCS_SECRET=<GCS_SECRET value>
```

This will add two environment variables MY_GCS_KEY and MY_GCS_SECRET to your runs. You can then access your bucket using a [libcloudObjectStore](https://libcloud.readthedocs.io/en/stable/storage/drivers/google_storage.html#libcloud.storage.drivers.google_storage.GoogleStorageDriver) object in your code with the following initialization:

```python
from libcloud.storage.drivers.google_storage import GoogleStorageDriver
import os

driver = GoogleStorageDriver(key=os.environ['GCS_KEY'], secret=os.environ['GCS_SECRET'],...)
```

(mcli/run_commands/integrations:github)=
### Github

Github SSH secrets will give you access to a private Github repository within the runtime environment.

First, see the instructions [here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account) to add a private key to your Github account.
**Make sure your SSH key does not have a password or the `git clone` will fail in the execution environment.**

Then, create a `git-ssh` secret using the SSH key you just attached to your Github account:

```bash
mcli create secret git-ssh ~/.ssh/my_id_rsa
```

This secret will set the `GIT_SSH_COMMAND` environment variable in your execution environment so that `git` will use your ssh key by default.
See the [Github integration](../run_commands/integrations.md#github) page for details on how to easily clone public or private Github repos.

<!-- TODO: checking script -->

```{note}
Because the `git-ssh` secret creates an environment variable for you, only one such secret is allowed.
If you need to have more, use the `ssh` secret type for the others instead.
```

```{note}
Depending on your Github repository's security settings, you may need to [enable SSO](https://docs.github.com/en/enterprise-cloud@latest/authentication/authenticating-with-saml-single-sign-on/authorizing-an-ssh-key-for-use-with-saml-single-sign-on) for your SSH key to work. 
```

### Huggingface

Huggingface is an open-source machine learning company that provides state-of-the-art ML models and tools for developers.

To enable Huggingface access within Databricks Mosiac AI platform, create an environment variable secret:

```bash
mcli create secret hf
```

Then, test that the API key was added correctly with a small test `script` below:

```yaml
name: huggingface-api-key
compute:
  gpus: 0
image: mosaicml/pytorch
integrations:
  - integration_type: pip_packages
    packages:
      - huggingface-hub
command: |
  export hf_token=$HUGGING_FACE_HUB_TOKEN
  echo "Checking if HF Token is set..."
  if [ -z "$hf_token" ]; then
    echo "Error: HF Token is empty"
    exit 1
  else
    echo "Logging in to Hugging Face..."
    huggingface-cli login --token $hf_token
    echo "Logged in. Running whoami to display the current user..."
    huggingface-cli whoami
  fi
```


### OCI

In order to stream data from Oracle Cloud Infrastructure (OCI) storage buckets when training models, MCLI will need access to your OCI credentials.

To set up OCI SSH keys and SDK, please consult the Oracle Cloud Infrastructure documentation [here](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/devguidesetupprereq.htm).
Specifically, there are two files you will need to generate or locate:

**1. Config File:** Locate the SDK/CLI configuration files using [this guide](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm#SDK_and_CLI_Configuration_File).
A sample config file would look like:

```
[DEFAULT]
user=ocid1.user.oc1..<unique_ID>
fingerprint=<your_fingerprint>
key_file=~/.oci/oci_api_key.pem
tenancy=ocid1.tenancy.oc1..<unique_ID>
region=us-ashburn-1

[ADMIN_USER]
user=ocid1.user.oc1..<unique_ID>
fingerprint=<your_fingerprint>
key_file=keys/admin_key.pem
pass_phrase=<your_passphrase>
```

**2. Key File:** Generate the required keys and OCIDs using [this guide](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.htm#Required_Keys_and_OCIDs).
The public key in PEM format looks something like this:

```
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQE...
...
-----END PUBLIC KEY-----
```

```{warning}
Your OCI private keys must be generated with no passphrases as runs are non-interactive.
```

Once both files are obtained, create the OCI secret with:

```bash
mcli create secret oci
```

Follow the prompts to name the secret and specify the location of the files:

```
> mcli create secret oci
? What would you like to name this secret? my-oci-secrets
? Where is your OCI config file located? ~/.oci/config
? Where is your OCI key file located? ~/.oci/oci_api_key.pem
✔  Created secret: my-oci-secrets
```

#### What happens when you run the above commands?

Once configured, we mount these secrets inside all of your runs and export three environment variables:

- `$OCI_CONFIG_FILE`: Path to your config file.
- `$OCI_CLI_CONFIG_FILE`: Path to the config file for using OCI through the CLI.
- `$OCI_CLI_KEY_FILE`: Path to your API signing private key file for using OCI through the CLI.

Libraries like [OCI](https://docs.oracle.com/en-us/iaas/tools/python/latest) will use these environment variables by default to discover your OCI credentials.

### AWS S3

In order to stream data from S3 buckets when training models, MCLI will need access to your AWS S3 credentials.

First, make sure the `awscli` is installed, and then run `aws configure` to create the config and credential files:

```bash
python -m pip install awscli
aws configure
```

Note: the requested credentials can be retrieved through your AWS console, typically under "Command line or programmatic access".

To add S3 credentials to MCLI, use the following command:

```bash
mcli create secret s3
```

This command produces the following output:

```bash
> mcli create secret s3
? What would you like to name this secret? my-s3-credentials
? Where is your S3 config file located? ~/.aws/config
? Where is your S3 credentials file located? ~/.aws/credentials
✔  Created secret: my-s3-credentials
```

The values for each of these queries can be passed as arguments using the `--name`, `--config-file` and `--credentials-file` arguments, respectively.
Your config and credentials files should follow the standard structure output by `aws configure`:

`~/.aws/config`

```
[default]
region=us-west-2
output=json
```

`~/.aws/credentials`

```
[default]
aws_access_key_id=AKIA...
aws_secret_access_key=EXAMPLE
```

More details on these files can be found [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).

Once you've created an S3 secret, we mount these secrets inside all of your runs and export two environment variables:

- `$AWS_CONFIG_FILE`: Path to your config file
- `$AWS_SHARED_CREDENTIALS_FILE`: Path to your credentials file

Libraries like [boto3](https://aws.amazon.com/sdk-for-python/) will use these environment variables by default to discover your S3 credentials.

### SSH Keys

Private SSH keys can be created that allow users to:

- SSH access to other available servers
- Clone a [private git repo](#github)
<!-- - Download and upload data with an [SFTP server](#sftp-ssh-secrets) -->

We have three SSH secret types for the above use cases: a generic `ssh` secret, `git-ssh` secret, or `sftp-ssh` secret. All three types mount your SSH private key as a file within your runs.

`git-ssh` and `sftp-ssh` are special commands that also set environment variables in addition to mounting SSH key files. Other than that, their configuration options are the same as a normal `ssh` key.

To see a full list of configuration options, you can run `mcli create secret git-ssh --help` or
`mcli create secret sftp-ssh --help`.

```{warning}
Your **SSH private keys must have no password** as runs are non-interactive.
```

#### Introduction to SSH Secrets

To create a simple SSH key:

```bash
mcli create secret ssh ~/.ssh/my_id_rsa
```

The above will store your private SSH key (given by the path `~/.ssh/my_id_rsa`) in our secure secret manager, printing out the name under which it is stored.
By default, the name will be the file stem (`my_id_rsa` in this case), but that can be customized with the `--name` argument.

```bash
mcli create secret ssh ~/.ssh/my_id_rsa --name my-ssh
```

By default, the SSH key will be mounted within your workload at `/secrets/<secret-name>/secret`.
This mount path can be changed by supplying the `--mount-path` argument.

The mount path will also be stored under the environment variable `SECRET_PATH_<UPPER_NAME>` where `<UPPER_NAME>` is the secret name, all upper-case with "-" replaced by "\_".

For example, the following run YAML will show output of `ls -l` of the mounted SSH private key.

```yaml
name: check-ssh
gpu_type: none
image: bash
command: |
  ls -l $SECRET_PATH_MY_ID_RSA
```

```{admonition} Multiple clusters
Note, if you have access to multiple clusters, specify `cluster: <cluster-name>` to choose one to run the test on. All of your secrets are available across all of your clusters.
```

Running this with `mcli run -f check-ssh.yaml` yields:

```
> mcli run -f check-ssh.yaml

i  Run check-ssh-ms5i submitted. Waiting for it to start...
i  You can press Ctrl+C to quit and follow your run manually.
✔  Run check-ssh started
i  Following run logs. Press Ctrl+C to quit.

lrwxrwxrwx    1 root     root            13 Jun  8 00:17 /secrets/my-id-rsa/secret -> ..data/my-id-rsa
```

#### Git SSH Secrets

`git-ssh` secrets work exactly like regular `ssh` secrets as described above except adding a `git-ssh` secret also
sets the `GIT_SSH_COMMAND` environment variable in your execution environment so that `git` will use your
SSH key by default.

Creating a `git-ssh` secret is the same as a normal `ssh` secret:

```bash
mcli create secret git-ssh ~/.ssh/my_id_rsa
```

```{admonition} Adding an SSH Key to Github
To add the provided private key to Github, see the instructions [here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account). **Make sure your SSH key does not have a password or the `git clone` will fail
in the execution environment.**
```

```{note}
Because the `git-ssh` secret creates an environment variable for you, only one such secret is allowed.
If you need to have more, use the `ssh` secret type for the others instead.
```

```{note}
Depending on your Github repository's security settings you may need to [enable sso](https://docs.github.com/en/enterprise-cloud@latest/authentication/authenticating-with-saml-single-sign-on/authorizing-an-ssh-key-for-use-with-saml-single-sign-on) for your SSH key to work.
```

#### SFTP SSH Secrets

`sftp-ssh` are the same as `ssh` secrets except the `COMPOSER_SFTP_KEY_FILE` environment variable will also set, which points to your key file. This allows using SFTP with [Composer](https://docs.mosaicml.com) without needing to provide additional credentials in your code.

```bash
mcli create secret sftp-ssh ~/.ssh/my_id_rsa
```

Furthermore, adding an `sftp-ssh` secret also adds the host fingerprint of the SFTP server to a `known_hosts` file in the execution environment and sets the environment variable `COMPOSER_SFTP_KNOWN_HOSTS_FILE` pointing to that file path. This simplifies the setup for using SFTP servers.

```{note}
Because the `sftp-ssh` secret creates a environment variables for you, only one such secret is allowed.
If you need to have more, use the `ssh` secret type for the others instead.
```



### Weights & Biases

Weights & Biases, a popular experiment tracking tool, reads its API Key from an environment variable named `WANDB_API_KEY`.

To enable this within the Databricks Mosaic AI training platform, create an environment variable secret as:

```bash
mcli create secret env --name wandb WANDB_API_KEY=<your-wandb-api-key>
```

Then, test the API key was added correctly with a small test `wandb login` call:

```yaml
name: wandb-login
compute:
  gpus: 0
image: python
integrations:
  - integration_type: pip_packages
    packages:
      - wandb
command: |
  wandb login
```

If secret registration was successful and your API key works, then you should see an output like the following on the command line of your test run's log:
```bash
wandb: Currently logged in as: <wandb user name>
```