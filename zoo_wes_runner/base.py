"""Base classes for Zoo runners.

These are derived here from the zoo-calrissian-runner because no generic abstract classes exist.
"""

import logging
import types

# Add zoo-calrissian-runner to path
# import os
# import sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../zoo-calrissian-runner')))
from zoo_calrissian_runner import ZooCalrissianRunner

try:
    import zoo
except ImportError:
    # Use centralized ZooStub from zoo-runner-common package
    from zoo_runner_common.zoostub import ZooStub

    zoo = ZooStub()

logger = logging.getLogger()


class BaseZooRunner(ZooCalrissianRunner):
    """Mangle the ZooCalrissianRunner to be a base class to inherit from."""

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
        """This function should be implemented to provide job execution logic."""
        raise NotImplementedError
