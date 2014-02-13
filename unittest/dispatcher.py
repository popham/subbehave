from ..command.base import DescribeModel, InjectResource, ScopeTransition
from ..dispatcher import Dispatcher

def build_dispatcher(behave_config, suite, context):
    command_queue = behave_config.command_queue
    return_queue = behave_config.return_queue
    d = Dispatcher(command_queue, return_queue)

    d.register(lambda c: isinstance(c, DescribeModel), context)
    d.register(lambda c: isinstance(c, InjectResource), suite)
    d.register(lambda c: isinstance(c, ScopeTransition), suite)

    return d
