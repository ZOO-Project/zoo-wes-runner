import json
import logging
import os
import time

import httpx
import yaml

from . import base

logger = logging.getLogger()


class ZooWESRunner(base.BaseZooRunner):
    """We wrap the base zoo runner but add our own execution step."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialise a httpx client to re-use.
        self.basic_auth = httpx.BasicAuth(
            os.environ.get("WES_USER"), os.environ.get("WES_PASSWORD")
        )
        self.httpx = httpx.Client(
            base_url=os.environ.get("WES_URL"), auth=self.basic_auth, trust_env=False
        )

        logger.error(self.inputs)

    def execute(self):
        """Execute some CWL on a WES Server."""
        if not self.assert_parameters():
            logger.error("Mandatory parameters missing")
            return base.zoo.SERVICE_FAILED

        # Prepare the CWL.
        cwljob = self.prepare()

        # Submit the job.
        response = self.httpx.post(
            "/runs",
            data={
                "workflow_url": "job.cwl",
                "workflow_type": "cwl",
                "workflow_type_version": "v1.0",
                "workflow_params": json.dumps(cwljob.params),
            },
            files={"workflow_attachment": ("job.cwl", yaml.dump(cwljob.cwl, encoding="utf-8"))},
        )
        # If the response wasn't 200, something went wrong. Exit.
        if response.status_code != 200:
            logger.error("Process request failed.")
            logger.error(response)
            logger.error(response.json())
            return base.zoo.SERVICE_FAILED

        # Store the run_id so we can watch the job.
        run_id = response.json()["run_id"]

        self.update_status(progress=20, message="execution submitted")

        # Watch the submitted job to see if it fails.
        state = "QUEUED"
        while state in ["QUEUED", "INITIALIZING", "RUNNING"]:
            logger.warning("Checking status of job")
            response = self.httpx.get(f"/runs/{run_id}/status")
            logger.warning(response.json())
            state = response.json()["state"]
            time.sleep(self.monitor_interval)
            logger.warning(f"Response json: {response.json()}")


            if state == "QUEUED":
                self.update_status(progress=21, message="Job has been queued on the HPC.")
            if state == "INITIALIZING":
                self.update_status(progress=22, message="Job is initializing on the HPC.")
            if state == "RUNNING":
                self.update_status(progress=50, message="Job is running on the HPC.")

        self.update_status(progress=90, message="Job has finished on the HPC.")
        # Once the job has finished, we exit with success if TOIl reports complete,
        # Otherwise, fail.
        if state == "COMPLETE":
            exit_value = base.zoo.SERVICE_SUCCEEDED
        else:
            exit_value = base.zoo.SERVICE_FAILED

        # Get the outputs and log.
        self.update_status(progress=90, message="successful.")
        response = self.httpx.get(f"/runs/{run_id}")
        json_response = response.json()
        self.demo_outputs = json_response.get("outputs", {})
        self.run_log = json_response.get("run_log", {})
        self.run_log_content = self.httpx.get(f"/runs/{self.run_log['stderr']}").text

        # Final status update then exit.
        self.update_status(progress=100, message="successful.")
        return exit_value
