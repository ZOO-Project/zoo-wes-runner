## Prerequisites

 * A user account which is able to submit jobs into SLURM. In the examples, this is `eoepca-toil`.
 * Shared storage which is mounted on all the SLURM nodes. In the examples, this is `/opt/toil/toil_storage`.

## Installation and Setup
### Install TOIL

 * Make directories for toil: `mkdir -p /opt/toil/toil_storage && cd /opt/toil`
 * Create a venv for the toil install `python3 -m venv environ && cd source environ/bin/activate`
 * Install toil into the environ `python3 -m pip install toil[all]`

### Install apptainer (formerly singularity) on all the SLURM nodes.
* `yum install apptainer apptainer-suid` on every node.

## Checking TOIL is working in your environment
Before continuing, you should check that TOIL jobs work when you submit them locally, and use this to iterate on the extra parameters you need to give to TOIL (eg default memory allocation, batch system) to get this to work on your system.

An example set of steps which works on our system is given below:

````
# Clone repository
git clone -b develop https://github.com/gfenoy/eoepca-zoo-wes-runner.git
# Move to the right location
cd eoepca-zoo-wes-runner
# Create the required directories
mkdir -p toil_storage/example/{work_dir,job_store}
# Execute a CWL Application Package using slurm batchSystem
toil-cwl-runner \
	--batchSystem slurm \
	--defaultMemory 500Mi \
	--maxMemory 100Gi \
	--singularity \
	--workDir toil_storage/example/work_dir \
	--jobStore toil_storage/example/job_store/$(uuidgen) \
	extras/example/app-package.cwl#water_bodies \
	extras/example/params.yaml
````

Additional parameters you can give to toil-cwl-runner are given [here](https://toil.readthedocs.io/en/latest/running/cliOptions.html)

## Configuring and starting the TOIL server
To start TOIL in server mode, some additional configuration is required.
A number of services must be started, as described [here](https://toil.readthedocs.io/en/latest/running/server/wes.html).
All of these commands are run on the same SLRUM headnode.

### Start a rabbitmq server
#### With Docker
Toil's celery worker requires a rabbitmq broker. You cn start this with docker using the following command:
```bash
docker run -d --restart=always \
	--name toil-wes-rabbitmq \
	-p 127.0.0.1:5672:5672 rabbitmq:3.9.5
```

#### With Apptainer
If apptainer is available but no docker, use the command below:
```bash
apptainer run \
    --bind $(pwd)/etc:/opt/bitnami/rabbitmq/etc/rabbitmq/ \
    --bind $(pwd)/var_lib:/opt/bitnami/rabbitmq/var/lib/rabbitmq \
    --bind $(pwd)/.rabbitmq:/opt/bitnami/rabbitmq/.rabbitmq/ \
    --bind $(pwd)/tmp:/bitnami/rabbitmq/ \
    docker://bitnami/rabbitmq:latest
```

### Start TOIL's Celery worker

#### Without systemd 
* Edit the file venv3.11/lib/python3.11/site-packages/toil/server/celery_app.py and replace user as username and password with the one you defined in the rabbitmq server (per default, you can use `user` as username and `bitnami` as password).

```bash
source ~/venv3.11/bin/activate
celery --broker=amqp://user:bitnami@127.0.0.1:5672// \
	-A toil.server.celery_app worker \
	--loglevel=INFO
```

#### With systemd

This will be started using a systemd unit.

 * Copy `extras/toil-celery.service` to `/etc/systemd/system`
 * Configure this file to run as the appropriate user, and to call toil from the appropriate location if you are not using the location above.
 * `systemctl daemon-reload && systemctl start toil-celery && systemctl enable toil-celery`

### Start the TOIL WES Server

#### Without systemd
The WES server can be started with the following command:

```bash
source ~/venv3.11/bin/activate 
TOIL_WES_BROKER_URL=amqp://user:bitnami@127.0.0.1:5672//  toil server \
	--opt=--batchSystem=slurm \
	--opt=--defaultMemory=500Mi \
	--opt=--maxMemory=100Gi \
	--opt=--singularity 
```

With these options, we ensure that the singularity container will be executed through SLURM.

#### With systemd
This will be started using a systemd unit.

 * Copy `extras/toil-server.service` to `/etc/systemd/system`
 * Configure this file to run as the appropriate user, and to call toil from the appropriate location if you are not using the location above.
 * You should adjust the `--opt` options to those which were required to run TOIL in the "Checking TOIL is working in your environment" step above, and you can add other options if you wish.
 * `systemctl daemon-reload && systemctl start toil-server && systemctl enable toil-server`

### Reverse proxy the WES API Using ngix.
The TOIL WES API is exposed through a reverse proxy, which allows us to add basic authentication to the API.

 * `yum install nginx && cd /etc/nginx`
 * Create a basic auth user and password for toil: `htpasswd ./htpasswd toil-username` and make a password. Make sure you note the password down.
 * Configure nginx using the configuration snippet in `extras/nginx.conf`. You should makse sure https is used to secure the authentication.
 * Expose nginx port you configured abover (probably 443) through the firewall.


