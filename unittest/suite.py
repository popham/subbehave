from io import BytesIO
from multiprocessing import Process, Queue
from unittest.suite import BaseTestSuite

from behave.configuration import Configuration
from behave.formatter.base import StreamOpener
from behave.formatter.formatters import register

from ..command.base import DescribeModel, InjectResource, ScopeTransition
from ..dispatcher import Dispatcher
from ..formatter import BlockingFormatter
from ..runner import ProcessRunner
from .case import StepTestCase
from .command import Result

register(BlockingFormatter)

class Context(object):
    def __init__(self):
        self.feature = None

    @property
    def feature(self):
        return self.__feature
    @feature.setter
    def feature(self, value):
        self.__feature = value
        self.scenario = None

    @property
    def scenario(self):
        return self.__scenario
    @scenario.setter
    def scenario(self, value):
        self.__scenario = value
        self.step = None

    def __str__(self):
        return '%s\n%s\n%s' % (self.feature, self.scenario, self.step)

class StepStream(object):
    def __init__(self, context, dispatcher):
        self.context = context
        self._dispatcher = dispatcher

    def __next__(self):
        self._dispatcher.prime()
        return StepTestCase(self.context, self._dispatcher.next_command_caller)

class BehaveSuite(BaseTestSuite):
    def __init__(self, features_directories):
        if isinstance(features_directories, str):
            features_directories = [features_directories]

        # Set up the Behave process.
        config = BehaveSuite.configuration(features_directories)
        #parametrize capture (in static config fn?)
        runner = ProcessRunner(config)
        self.behave_process = Process(target=runner.run)

        # Set up the Behave process's consumer.
        self._resources = []
        self._context = Context()

        terminal = lambda c: isinstance(c, ResultCommand)
        self._dispatcher = Dispatcher(config.command_queue, config.return_queue, terminal)

        d = self._dispatcher
        d.register(lambda c: isinstance(c, ScopeTransition), self)
        d.register(lambda c: isinstance(c, Resource), self)
        d.register(lambda c: isinstance(c, DescribeModel), self._context)

    def __repr__(self):
        return '<BehaveSuite>'

    def pushScope(self):
        self._resources.append([])
        self._dispatcher.push()

    def popScope(self):
        self._dispatcher.pop()
        for r in self._resources.pop():
            r.destroy()

    def attachResource(self, resource):
        resource.create()
        resource.register(self._dispatcher)
        self._resources[-1].append(resource)

    def __iter__(self):
        return StepStream(self._context, self._dispatcher)

    def run(self, result):
        self.behave_process.start()
        result = super().run(result)
        self.behave_process.join()

        return result

    @staticmethod
    def configuration(features_directories):
        config = Configuration()
        config.command_queue = Queue()
        config.return_queue = Queue()
        config.show_snippets = False
        config.summary = False
        config.format = ['blocking.pretty']
        config.outputs = [StreamOpener(stream=BytesIO())] # Clobber stdout
        config.reporters = []
        config.paths = features_directories

        return config
