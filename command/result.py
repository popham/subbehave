from .base import Result, StepModel

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
