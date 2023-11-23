import json
import logging
import time

import httpx
import yaml

from . import base

logger = logging.getLogger()


class ZooWESRunner(base.BaseZooRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Todo: what is the proper way to pass through the config from Zoo?
        wes_url = "http://192.168.3.146/ga4gh/wes/v1/"
        user = "some-user"
        password = "some-password"

        # Initialise a httpx client to re-use.
        self.httpx = httpx.Client(base_url=wes_url, auth=(user, password), trust_env=False)

    def execute(self):
        """Execute some CWL on a WES Server."""
        if not self.assert_parameters():
            logger.error("Mandatory parameters missing")
            return base.zoo.SERVICE_FAILED

        cwljob = self.prepare()

        # Submit the job.
        # Todo: how do we get the correct URL with the #fragment ?
        # Todo: are the cwl and params from pre_execute always json/yaml dumpable?
        # Todo: maybe some of these need to be configurable.
        response = self.httpx.post(
            "/runs",
            data={
                "workflow_url": "job.cwl#water_bodies",
                "workflow_type": "cwl",
                "workflow_type_version": "v1.0",
                "workflow_params": json.dumps(cwljob.params),
            },
            files={"workflow_attachment": ("job.cwl", yaml.dump(cwljob.cwl, encoding="utf-8"))},
        )
        if response.status_code != 200:
            logger.warning(response)
            logger.warning(response.json())
            # todo: how do we raise an error that zoo can understand.

        logger.warning(response)
        logger.warning(response.json())
        run_id = response.json()["run_id"]

        self.update_status(progress=18, message="execution submitted")

        # Watch the submitted job to see if it fails.
        # Todo: perhaps send an self.update_status when the job moves from queued, to init to running.
        state = "QUEUED"
        while state in ["QUEUED", "INITIALIZING", "RUNNING"]:
            response = httpx.get(f"/runs/{run_id}/status")
            state = response.json()["state"]
            time.sleep(self.monitor_interval)

        # When the job has finished, find out what happened.
        response = httpx.get(f"/runs/{run_id}/")
        result = response.json()

        if result["state"] == "COMPLETE":
            exit_value = base.zoo.SERVICE_SUCCEEDED
        else:
            exit_value = base.zoo.SERVICE_FAILED

        # todo: what outputs are required, and what format do they need to be in?
        # todo: we can probably come up with a simple usage report by combining slurm resources and runtime.
        self.outputs.set_output(result)

        return exit_value
