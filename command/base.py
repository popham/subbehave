class Complete(object):
    pass

class Command(object):
    def trigger(self, config):
        config.command_queue.put(self)
        completion = config.return_queue.get()
        assert isinstance(completion, Complete)

    @classmethod
    def vacuous_return(cls, return_queue):
        return_queue.put(Complete())

class ScopeTransition(Command):
    def __call__(self, return_queue, suite):
        raise NotImplementedError

class DescribeModel(Command):
    def __call__(self, return_queue, context):
        raise NotImplementedError

class InjectResource(Command):
    def __call__(self, return_queue, owner):
        raise NotImplementedError

class StepModel(object):
    def __init__(self, step):
        self.name          = step.name
        self.text          = step.text
        self.type          = step.step_type
        self.filename      = step.filename
        self.line          = step.line
        self.status        = step.status
        self.error_message = step.error_message

    def __str__(self):
        return '%s: %s\n  (%s:%s)' % (
            self.type,
            self.name,
            self.filename,
            self.line)

class Result(Command, StepModel):
    def __init__(self, step, capture):
        super().__init__(step)
        self.capture = capture

    def __call__(self, return_queue, test, pyunit_result):
        raise NotImplementedError
