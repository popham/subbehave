from .base import ScopeTransition

class Open(ScopeTransition):
    def __call__(self, return_queue, suite):
        suite.pushScope()
        self.vacuous_return(return_queue)

class Start(Open):
    pass

class Close(ScopeTransition):
    def __call__(self, return_queue, suite):
        suite.popScope()
        self.vacuous_return(return_queue)

class Stop(Close):
    def __call__(self, return_queue, suite):
        super().__call__(return_queue, suite)
        raise StopIteration
