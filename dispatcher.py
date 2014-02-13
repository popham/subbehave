import functools
import itertools

from .command.base import Result
class UnhandledCommand(TypeError):
    def __init__(self, command):
        msg = 'Cannot handle command. Provided: %s'
        super().__init__(msg % command.__class__)

class Dispatcher(object):
    def __init__(self, command_queue, return_queue):
        self.__command_queue = command_queue
        self.__return_queue = return_queue
        self.__terminal = lambda c: isinstance(c, Result)
        self.__handlers = [[]]

    def register(self, matcher, arg):
        self.__handlers[-1].append((matcher,arg))

    def push(self):
        self.__handlers.append([])

    def pop(self):
        self.__handlers.pop()

    def prime(self):
        peek = self.__command_queue.get()
        while not self.__terminal(peek):
            hs = list(itertools.chain(*self.__handlers))
            hs.reverse() # Bias the choice toward top of stack.
            _, arg = next(filter(lambda pair: pair[0](peek), hs), (None,None))
            if arg is not None:
                peek(self.__return_queue, arg)
            else:
                raise UnhandledCommand(peek)
            peek = self.__command_queue.get()
        self.__command_queue.put(peek) # Leave the terminal in the queue.

    @property
    def next_command_caller(self):
        c = self.__command_queue.get()
        return functools.partial(c, self.__return_queue)
