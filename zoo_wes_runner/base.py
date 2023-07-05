"""Bases classes for Zoo runners.

These are derived here from the zoo-calrissian-runner because no generic abstract classes exist.
"""
import logging
import types

import zoo_calrissian_runner

logger = logging.getLogger()

# todo: where does zoo come from?
zoo = zoo_calrissian_runner.zoo


class BaseZooRunner(zoo_calrissian_runner.ZooCalrissianRunner):
    """Mangle the ZooCalrissianRunner to be a base class to inherit from."""

    def __new__(cls):
        """Create a ZooRunner without kubernetes-specific things."""
        cls.shorten_namespace = None
        cls.get_namespace_name = None
        return cls

    def prepare(self):
        """Generic pre-execution steps which might apply to all handlers."""

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
