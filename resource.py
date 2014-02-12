class Resource(object):
    command_type = None

    def create(self):
        raise NotImplementedError

    def register(self, dispatcher):
        dispatcher.register(lambda c: isinstance(c, self.command_type), self)

    def destroy(self):
        raise NotImplementedError
