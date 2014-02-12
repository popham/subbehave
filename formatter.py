from behave.formatter.pretty import PrettyFormatter

from .command.describe_model import Feature, Scenario, Step
from .command.result import *

class BlockingFormatter(PrettyFormatter):
    name = 'blocking.pretty'
    description = 'Color formatter that dispatches to a Unittest backend'
    results = {
        'passed'    : Succeed,
        'skipped'   : Skip,
        'failed'    : Fail,
        'undefined' : Undefined,
        'untested'  : Untested}

    def feature(self, feature):
        super().feature(feature)
        Feature(feature).trigger(self.config)

    def scenario(self, scenario):
        super().scenario(scenario)
        Scenario(scenario).trigger(self.config)

    def step(self, step):
        super().step(step)
        Step(step).trigger(self.config)

    def result(self, step_result):
        self.stream.truncate(0)
        super().result(step_result)
        capture = self.stream.getvalue().decode()

        Result = self.results.get(step_result.status, None)
        if Result:
            Result(step_result, capture).trigger(self.config)
        else:
            msg = 'Unhandled result status: %s'
            raise NotImplementedError(msg % step_result.status)
