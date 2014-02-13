from ..command.base import Command, StepModel

class Result(Command, StepModel):

    """
    `PyunitResult` protocol interface.

    `PyunitResult` instances describe a step result to a `unittest` consumer.

    """

    def __init__(self, step, capture):
        """
        Extend `StepModel` with captured stream data from Behave.

        :param step: `Step` instance from Behave.
        :param capture: String data captured by Behave's stream capture
        mechanics.
        """
        super().__init__(step)
        self.capture = capture

    def __call__(self, return_queue, test, pyunit_result):
        """
        Execute the command.

        :param return_queue: `Queue` to receive `Complete` instance upon
        completion of command handling.
        :param test: `StepTestCase` instance
        :param pyunit_result: `

        """
        raise NotImplementedError

class Succeed(Result, StepModel):
    def __call__(self, return_queue, test, pyunit_result):
        pyunit_result.addSuccess(test)
        self.vacuous_return(return_queue)

class Skip(Result, StepModel):
    def __call__(self, return_queue, test, pyunit_result):
        # Unittest's addSkip signature requires a reason argument. This message
        # is a little tautological...
        msg = 'Skipped Step: %s %s.'
        pyunit_result.addSkip(test, msg % (self.type.upper(), self.name))
        self.vacuous_return(return_queue)

class Untested(Skip):
    def __call__(self, return_queue, test, pyunit_result):
        # Another tautological message...
        msg = 'Untested Step: %s %s.'
        pyunit_result.addSkip(test, msg % (self.type.upper(), self.name))
        self.vacuous_return(return_queue)

class Fail(Result, StepModel):
    def __call__(self, return_queue, test, pyunit_result):
        msg = self.error_message.strip()
        pyunit_result.addFailure(test, msg)
        self.vacuous_return(return_queue)

class Undefined(Fail):
    def __call__(self, return_queue, test, pyunit_result):
        msg = 'Undefined Step: %s %s'
        pyunit_result.addFailure(test, msg % (self.type.upper(), self.name))
        self.vacuous_return(return_queue)
