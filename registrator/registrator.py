class _Registrator:
    def __init__(self):
        self.handlers = dict()

    def set_handlers(self, server):
        server.handlers = self.handlers

    def register(self, key, handler):
        self.handlers[key] = handler

    def __call__(self, key):
        def dercorator(handler):
            self.handlers[key] = handler
        return dercorator

Registrator = _Registrator()

class _Service_Registrator:
    def __init__(self):
        self.services = []

    def set_services(self, server):
        server.services = self.services
        
    def register(self, service):
        self.services.append(service)

    def __call__(self, service):
        self.services.append(service)


ServiceRegistrator = _Service_Registrator()
