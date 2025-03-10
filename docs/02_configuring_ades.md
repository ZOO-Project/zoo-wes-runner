## Configuring the ZOO-Project-DRU.

The ZOO-Project-DRU must be configured to do the following:

 * Run an ZOO-Project docker image which has the python packaged contained in this repo installed.
 * Use the cookiecutter from [here](https://github.com/EOEPCA/eoepca-proc-service-template-wes/) instead of the one for calrissian.
 * Pass the URL and basic auth information as environment variables into the image.

A minimal example of the helm values required to do this is contained in `examples/zoo-dru-values.yaml`. These are indended to be applied to the zoo-dru helm chart [here](https://github.com/ZOO-Project/charts/tree/main/zoo-project-dru)- you will likely need to customise the other values to match your setup and environment.

Once you have a complete values file, this can be installed into your kubernetes cluster with the following command:

````
helm upgrade --install \
    --create-namespace --namespace zoo zoo-project-dru \
    zoo-project/zoo-project-dru \
    --version 0.1.1 \
    --values ./values.yaml
````

### Create SSH tunnels (optional)

We use OpenSSH tunnels to provide remote access from the Kubernetes cluster to the HPC and vice versa.

First, we must use the following command to access the remote WES running on an identified login node (e.g., login02).

````
# Access to WES
ssh -i myOpenSSH.key \
    -L 0.0.0.0:8100:127.0.0.1:8080 \
    <user>@login02.hpc.ressources.name
````

We also need to provide access to the S3 bucket on our cluster from the HPC. This bucket stores the execution's final results.

````
# Access to S3 bukect
ssh -i myOpenSSH.key \
    -R 0.0.0.0:4900:127.0.0.1:4566 \
    <user>@login02.hpc.ressources.name
````

Some HPC login nodes do not allow opening ports on any IP address. Consequently, using the previous command will open the port in LISTEN mode only on the loopback address (127.0.0.1), which is unreachable from the SBATCH environment. In such cases, we should use a public address to access the S3 bucket.