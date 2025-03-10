## Zoo-WES-Runner

This repository is a plugin for the [ZOO-Project](https://github.com/ZOO-Project/ZOO-Project), which allows it submit jobs to a [Workflow Execution Service (WES)](https://ga4gh.github.io/workflow-execution-service-schemas/docs/).
This allows the ZOO-Project to submit jobs to run in a number of different environments.

This work is undertaken as part of the deployment of the [EOEPCA](https://ga4gh.github.io/workflow-execution-service-schemas/docs/) on [JASMIN](https://jasmin.ac.uk).

It has been developed using the EOEPCA ADES connected to the [TOIL](toil.readthedocs.io) workflow engine running workflows using singularity in a SLURM cluster.
However, the TOIL WES server supports many other configurations, such as support for a number of batch systems (Grid Engine, Torque and LSF), cloud platforms, local execution on the server, etc. It should be possible to use this module with any configuration in which TOIL can run workflows, or indeed a different WES server other than TOIL. However, these configurations have not been tested.

This documentation is split into a number of parts:
1. Configuring the TOIL server on a SLURM headnode.
1. Configuring EOEPCA to use the TOIL server.
1. Submitting jobs and debugging.
