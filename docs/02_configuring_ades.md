## Configuring the ADES.

The ADES must be configured to do the following:
* Run an ADES docker image which has the python packaged contained in this repo installed.
* Use the cookiecutter from [here](https://github.com/cedadev/eoepca-proc-service-template-wes/) instead of the one for calrissian.
* Pass the URL and basic auth information as environment variables into the image.

A minimal example of the helm values required to do this is contained in `examples/zoo-dru-values.yaml`. These are indended to be applied to the zoo-dru helm chart [here](https://github.com/ZOO-Project/charts/tree/main/zoo-project-dru)- you will likely need to customise the other values to match your setup and environment.

Once you have a complete values file, this can be installed into your kubernetes cluster with the following command:
`helm upgrade --install --create-namespace --namespace zp zoo-dru zoo-project/zoo-project-dru --version 0.1.1 --values ./values.yaml`
