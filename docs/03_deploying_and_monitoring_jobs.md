## Monitoring
* You can call zoo's `/<user>/ogc-api/jobs/<job-id>` endpoint to find out the status of your job, if it succeeded or failed.

## Debugging
* Logs are stored in the ADES zoo-fpm pod, in the conainter called zoofpm.
* Once a workflow is deployed, the cookiecutter will be run and the output stored in `/opt/zooservice_user`
* When a workflow is run, python errors and output are available at `/var/ww/html/temp`, which two files created for each run, named for the job ID. There is an error log, and a json status file.

* To check TOIL has recieved the job, you can look at the TOIL logs. If you have followed the configuration instructions in this directory, you can look at these using `journalctl -u toil-server.service` on the TOIL machine.
* It is sometimes also useful to look in TOIL's server working directoty, where job status is kept.
* If you are running the jobs on SLURM, you can watch the SLURM queue to check jobs are created successfully.
