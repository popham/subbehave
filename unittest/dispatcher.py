def build_dispatcher(behave_config, suite, context):
    command_queue = behave_config.command_queue
    return_queue = behave_config.return_queue
    terminal = lambda c: isinstance(c, ResultCommand)

    d = Dispatcher(config.command_queue, config.return_queue, terminal)

    d.register(lambda c: isinstance(c, ScopeTransition), suite)
    d.register(lambda c: isinstance(c, Resource), suite)
    d.register(lambda c: isinstance(c, DescribeModel), context)

    return d
