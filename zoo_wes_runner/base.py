"""Bases classes for Zoo runners.

These are derived here from the zoo-calrissian-runner because no generic abstract classes exist.
"""
import logging
import types

import zoo
import zoo_calrissian_runner

logger = logging.getLogger()


class BaseZooRunner(zoo_calrissian_runner.ZooCalrissianRunner):
    """Mangle the ZooCalrissianRunner to be a base class to inherit from."""

    shorten_namespace = None
    get_namespace_name = None

    def prepare(self):
        """Generic pre-execution which applies to all handlers."""

        logger.info("execution started")
        self.update_status(progress=2, message="starting execution")

        logger.info("wrap CWL workflow with stage-in/out steps")

        processing_parameters = {
            **self.get_processing_parameters(),
            **self.handler.get_additional_parameters(),
        }
        return types.SimpleNamespace(cwl=self.wrap(), params=processing_parameters)

    def execute(self):
        raise NotImplementedError
